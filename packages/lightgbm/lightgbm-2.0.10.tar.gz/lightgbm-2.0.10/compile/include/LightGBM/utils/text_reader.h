#ifndef LIGHTGBM_UTILS_TEXT_READER_H_
#define LIGHTGBM_UTILS_TEXT_READER_H_

#include <LightGBM/utils/pipeline_reader.h>
#include <LightGBM/utils/log.h>
#include <LightGBM/utils/random.h>

#include <cstdio>
#include <sstream>

#include <vector>
#include <string>
#include <functional>

namespace LightGBM {

/*!
* \brief Read text data from file
*/
template<typename INDEX_T>
class TextReader {
public:
  /*!
  * \brief Constructor
  * \param filename Filename of data
  * \param is_skip_first_line True if need to skip header
  */
  TextReader(const char* filename, bool is_skip_first_line):
    filename_(filename), is_skip_first_line_(is_skip_first_line){
    if (is_skip_first_line_) {
      FILE* file;
#ifdef _MSC_VER
      fopen_s(&file, filename, "r");
#else
      file = fopen(filename, "r");
#endif
      if (file == NULL) {
        Log::Fatal("Could not open %s", filename);
      }
      std::stringstream str_buf;
      int read_c = -1;
      read_c = fgetc(file);
      while (read_c != EOF) {
        char tmp_ch = static_cast<char>(read_c);
        if (tmp_ch == '\n' || tmp_ch == '\r') {
          break;
        }
        str_buf << tmp_ch;
        ++skip_bytes_;
        read_c = fgetc(file);
      }
      if (static_cast<char>(read_c) == '\r') {
        read_c = fgetc(file);
        ++skip_bytes_;
      }
      if (static_cast<char>(read_c) == '\n') {
        read_c = fgetc(file);
        ++skip_bytes_;
      }
      fclose(file);
      first_line_ = str_buf.str();
      Log::Debug("Skipped header \"%s\" in file %s", first_line_.c_str(), filename_);
    }
  }
  /*!
  * \brief Destructor
  */
  ~TextReader() {
    Clear();
  }
  /*!
  * \brief Clear cached data
  */
  inline void Clear() {
    lines_.clear();
    lines_.shrink_to_fit();
  }
  /*!
  * \brief return first line of data
  */
  inline std::string first_line() {
    return first_line_;
  }
  /*!
  * \brief Get text data that read from file
  * \return Text data, store in std::vector by line
  */
  inline std::vector<std::string>& Lines() { return lines_; }

  INDEX_T ReadAllAndProcess(const std::function<void(INDEX_T, const char*, size_t)>& process_fun) {
    last_line_ = "";
    INDEX_T total_cnt = 0;
    PipelineReader::Read(filename_, skip_bytes_,
      [this, &total_cnt, &process_fun]
    (const char* buffer_process, size_t read_cnt) {
      size_t cnt = 0;
      size_t i = 0;
      size_t last_i = 0;
      // skip the break between \r and \n
      if (last_line_.size() == 0 && buffer_process[0] == '\n') {
        i = 1;
        last_i = i;
      }
      while (i < read_cnt) {
        if (buffer_process[i] == '\n' || buffer_process[i] == '\r') {
          if (last_line_.size() > 0) {
            last_line_.append(buffer_process + last_i, i - last_i);
            process_fun(total_cnt, last_line_.c_str(), last_line_.size());
            last_line_ = "";
          }
          else {
            process_fun(total_cnt, buffer_process + last_i, i - last_i);
          }
          ++cnt;
          ++i;
          ++total_cnt;
          // skip end of line
          while ((buffer_process[i] == '\n' || buffer_process[i] == '\r') && i < read_cnt) { ++i; }
          last_i = i;
        }
        else {
          ++i;
        }
      }
      if (last_i != read_cnt) {
        last_line_.append(buffer_process + last_i, read_cnt - last_i);
      }
      return cnt;
    });
    // if last line of file doesn't contain end of line
    if (last_line_.size() > 0) {
      Log::Info("Warning: last line of %s has no end of line, still using this line", filename_);
      process_fun(total_cnt, last_line_.c_str(), last_line_.size());
      ++total_cnt;
      last_line_ = "";
    }
    return total_cnt;
  }

  /*!
  * \brief Read all text data from file in memory
  * \return number of lines of text data
  */
  INDEX_T ReadAllLines() {
    return ReadAllAndProcess(
      [this](INDEX_T, const char* buffer, size_t size) {
      lines_.emplace_back(buffer, size);
    });
  }

  INDEX_T SampleFromFile(Random& random, INDEX_T sample_cnt, std::vector<std::string>* out_sampled_data) {
    INDEX_T cur_sample_cnt = 0;
    return ReadAllAndProcess(
      [this, &random, &cur_sample_cnt, &sample_cnt, &out_sampled_data]
    (INDEX_T line_idx, const char* buffer, size_t size) {
      if (cur_sample_cnt < sample_cnt) {
        out_sampled_data->emplace_back(buffer, size);
        ++cur_sample_cnt;
      }
      else {
        const size_t idx = static_cast<size_t>(random.NextInt(0, static_cast<int>(line_idx + 1)));
        if (idx < static_cast<size_t>(sample_cnt)) {
          out_sampled_data->operator[](idx) = std::string(buffer, size);
        }
      }
    });
  }
  /*!
  * \brief Read part of text data from file in memory, use filter_fun to filter data
  * \param filter_fun Function that perform data filter
  * \param out_used_data_indices Store line indices that read text data
  * \return The number of total data
  */
  INDEX_T ReadAndFilterLines(const std::function<bool(INDEX_T)>& filter_fun, std::vector<INDEX_T>* out_used_data_indices) {
    out_used_data_indices->clear();
    INDEX_T total_cnt = ReadAllAndProcess(
      [this, &out_used_data_indices, &filter_fun]
    (INDEX_T line_idx , const char* buffer, size_t size) {
      bool is_used = filter_fun(line_idx);
      if (is_used) { out_used_data_indices->push_back(line_idx); }
      if (is_used) { lines_.emplace_back(buffer, size); }
    });
    return total_cnt;
  }

  INDEX_T SampleAndFilterFromFile(const std::function<bool(INDEX_T)>& filter_fun, std::vector<INDEX_T>* out_used_data_indices,
    Random& random, INDEX_T sample_cnt, std::vector<std::string>* out_sampled_data) {
    INDEX_T cur_sample_cnt = 0;
    out_used_data_indices->clear();
    INDEX_T total_cnt = ReadAllAndProcess(
      [this, &out_used_data_indices, &filter_fun, &random, &cur_sample_cnt, &sample_cnt, &out_sampled_data]
    (INDEX_T line_idx, const char* buffer, size_t size) {
      bool is_used = filter_fun(line_idx);
      if (is_used) { out_used_data_indices->push_back(line_idx); }
      if (is_used) {
        if (cur_sample_cnt < sample_cnt) {
          out_sampled_data->emplace_back(buffer, size);
          ++cur_sample_cnt;
        }
        else {
          const size_t idx = static_cast<size_t>(random.NextInt(0, static_cast<int>(out_used_data_indices->size())));
          if (idx < static_cast<size_t>(sample_cnt) ) {
            out_sampled_data->operator[](idx) = std::string(buffer, size);
          }
        }
      }
    });
    return total_cnt;
  }

  INDEX_T CountLine() {
    return ReadAllAndProcess(
      [this](INDEX_T, const char*, size_t) {
    });
  }

  INDEX_T ReadAllAndProcessParallelWithFilter(const std::function<void(INDEX_T, const std::vector<std::string>&)>& process_fun, const std::function<bool(INDEX_T,INDEX_T)>& filter_fun) {
    last_line_ = "";
    INDEX_T total_cnt = 0;
    INDEX_T used_cnt = 0;
    PipelineReader::Read(filename_, skip_bytes_,
      [this, &total_cnt, &process_fun,&used_cnt, &filter_fun]
    (const char* buffer_process, size_t read_cnt) {
      size_t cnt = 0;
      size_t i = 0;
      size_t last_i = 0;
      INDEX_T start_idx = used_cnt;
      // skip the break between \r and \n
      if (last_line_.size() == 0 && buffer_process[0] == '\n') {
        i = 1;
        last_i = i;
      }
      while (i < read_cnt) {
        if (buffer_process[i] == '\n' || buffer_process[i] == '\r') {
          if (last_line_.size() > 0) {
            last_line_.append(buffer_process + last_i, i - last_i);
            if (filter_fun(used_cnt, total_cnt)) {
              lines_.push_back(last_line_);
              ++used_cnt;
            }
            last_line_ = "";
          }
          else {
            if (filter_fun(used_cnt, total_cnt)) {
              lines_.emplace_back(buffer_process + last_i, i - last_i);
              ++used_cnt;
            }
          }
          ++cnt;
          ++i;
          ++total_cnt;
          // skip end of line
          while ((buffer_process[i] == '\n' || buffer_process[i] == '\r') && i < read_cnt) { ++i; }
          last_i = i;
        }
        else {
          ++i;
        }
      }
      process_fun(start_idx, lines_);
      lines_.clear();
      if (last_i != read_cnt) {
        last_line_.append(buffer_process + last_i, read_cnt - last_i);
      }
      return cnt;
    });
    // if last line of file doesn't contain end of line
    if (last_line_.size() > 0) {
      Log::Info("Warning: last line of %s has no end of line, still using this line", filename_);
      if (filter_fun(used_cnt, total_cnt)) {
        lines_.push_back(last_line_);
        process_fun(used_cnt, lines_);
      }
      lines_.clear();
      ++total_cnt;
      ++used_cnt;
      last_line_ = "";
    }
    return total_cnt;
  }

  INDEX_T ReadAllAndProcessParallel(const std::function<void(INDEX_T, const std::vector<std::string>&)>& process_fun) {
    return ReadAllAndProcessParallelWithFilter(process_fun, [](INDEX_T, INDEX_T) { return true; });
  }

  INDEX_T ReadPartAndProcessParallel(const std::vector<INDEX_T>& used_data_indices, const std::function<void(INDEX_T, const std::vector<std::string>&)>& process_fun) {
    return ReadAllAndProcessParallelWithFilter(process_fun,
      [&used_data_indices](INDEX_T used_cnt ,INDEX_T total_cnt) {
      if (static_cast<size_t>(used_cnt) < used_data_indices.size() && total_cnt == used_data_indices[used_cnt]) {
        return true;
      }
      else {
        return false;
      }
    });
  }

private:
  /*! \brief Filename of text data */
  const char* filename_;
  /*! \brief Cache the read text data */
  std::vector<std::string> lines_;
  /*! \brief Buffer for last line */
  std::string last_line_;
  /*! \brief first line */
  std::string first_line_="";
  /*! \brief is skip first line */
  bool is_skip_first_line_ = false;
  /*! \brief is skip first line */
  int skip_bytes_ = 0;
};

}  // namespace LightGBM

#endif   // LightGBM_UTILS_TEXT_READER_H_

