#ifndef LIGHTGBM_UTILS_PIPELINE_READER_H_
#define LIGHTGBM_UTILS_PIPELINE_READER_H_

#include <LightGBM/utils/log.h>

#include <cstdio>

#include <functional>
#include <thread>
#include <memory>
#include <algorithm>

namespace LightGBM{

/*!
* \brief A pipeline file reader, use 2 threads, one read block from file, the other process the block
*/
class PipelineReader {
public:
  /*!
  * \brief Read data from a file, use pipeline methods
  * \param filename Filename of data
  * \process_fun Process function
  */
  static size_t Read(const char* filename, int skip_bytes, const std::function<size_t (const char*, size_t)>& process_fun) {
    FILE* file;

#ifdef _MSC_VER
    fopen_s(&file, filename, "rb");
#else
    file = fopen(filename, "rb");
#endif
    if (file == NULL) {
      return 0;
    }
    size_t cnt = 0;
    const size_t buffer_size =  16 * 1024 * 1024 ;
    // buffer used for the process_fun
    auto buffer_process = std::vector<char>(buffer_size);
    // buffer used for the file reading
    auto buffer_read = std::vector<char>(buffer_size);
    size_t read_cnt = 0;
    if (skip_bytes > 0) {
      // skip first k bytes
      read_cnt = fread(buffer_process.data(), 1, skip_bytes, file);
    }
    // read first block
    read_cnt = fread(buffer_process.data(), 1, buffer_size, file);
    size_t last_read_cnt = 0;
    while (read_cnt > 0) {
      // start read thread
      std::thread read_worker = std::thread(
        [file, &buffer_read, buffer_size, &last_read_cnt] {
        last_read_cnt = fread(buffer_read.data(), 1, buffer_size, file);
      }
      );
      // start process
      cnt += process_fun(buffer_process.data(), read_cnt);
      // wait for read thread
      read_worker.join();
      // exchange the buffer
      std::swap(buffer_process, buffer_read);
      read_cnt = last_read_cnt;
    }
    // close file
    fclose(file);
    return cnt;
  }

};

}  // namespace LightGBM

#endif   // LightGBM_UTILS_PIPELINE_READER_H_
