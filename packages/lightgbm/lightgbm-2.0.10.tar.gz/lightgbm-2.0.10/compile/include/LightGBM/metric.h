#ifndef LIGHTGBM_METRIC_H_
#define LIGHTGBM_METRIC_H_

#include <LightGBM/meta.h>
#include <LightGBM/config.h>
#include <LightGBM/dataset.h>
#include <LightGBM/objective_function.h>

#include <vector>

namespace LightGBM {

/*!
* \brief The interface of metric.
*        Metric is used to calculate metric result
*/
class Metric {
public:
  /*! \brief virtual destructor */
  virtual ~Metric() {}

  /*!
  * \brief Initialize
  * \param test_name Specific name for this metric, will output on log
  * \param metadata Label data
  * \param num_data Number of data
  */
  virtual void Init(const Metadata& metadata, data_size_t num_data) = 0;

  virtual const std::vector<std::string>& GetName() const = 0;

  virtual double factor_to_bigger_better() const = 0;
  /*!
  * \brief Calcaluting and printing metric result
  * \param score Current prediction score
  */
  virtual std::vector<double> Eval(const double* score, const ObjectiveFunction* objective) const = 0;

  Metric() = default;
  /*! \brief Disable copy */
  Metric& operator=(const Metric&) = delete;
  /*! \brief Disable copy */
  Metric(const Metric&) = delete;

  /*!
  * \brief Create object of metrics
  * \param type Specific type of metric
  * \param config Config for metric
  */
  LIGHTGBM_EXPORT static Metric* CreateMetric(const std::string& type, const MetricConfig& config);

};

/*!
* \brief Static class, used to calculate DCG score
*/
class DCGCalculator {
public:
  /*!
  * \brief Initial logic
  * \param label_gain Gain for labels, default is 2^i - 1
  */
  static void Init(std::vector<double> label_gain);

  /*!
  * \brief Calculate the DCG score at position k
  * \param k The position to evaluate
  * \param label Pointer of label
  * \param score Pointer of score
  * \param num_data Number of data
  * \return The DCG score
  */
  static double CalDCGAtK(data_size_t k, const float* label,
    const double* score, data_size_t num_data);

  /*!
  * \brief Calculate the DCG score at multi position
  * \param ks The positions to evaluate
  * \param label Pointer of label
  * \param score Pointer of score
  * \param num_data Number of data
  * \param out Output result
  */
  static void CalDCG(const std::vector<data_size_t>& ks,
    const float* label, const double* score,
    data_size_t num_data, std::vector<double>* out);

  /*!
  * \brief Calculate the Max DCG score at position k
  * \param k The position want to eval at
  * \param label Pointer of label
  * \param num_data Number of data
  * \return The max DCG score
  */
  static double CalMaxDCGAtK(data_size_t k,
    const float* label, data_size_t num_data);

  /*!
  * \brief Check the label range for NDCG and lambdarank
  * \param label Pointer of label
  * \param num_data Number of data
  */
  static void CheckLabel(const float* label, data_size_t num_data);

  /*!
  * \brief Calculate the Max DCG score at multi position
  * \param ks The positions want to eval at
  * \param label Pointer of label
  * \param num_data Number of data
  * \param out Output result
  */
  static void CalMaxDCG(const std::vector<data_size_t>& ks,
    const float* label, data_size_t num_data, std::vector<double>* out);

  /*!
  * \brief Get discount score of position k
  * \param k The position
  * \return The discount of this position
  */
  inline static double GetDiscount(data_size_t k) { return discount_[k]; }

private:
  /*! \brief store gains for different label */
  static std::vector<double> label_gain_;
  /*! \brief store discount score for different position */
  static std::vector<double> discount_;
  /*! \brief max position for eval */
  static const data_size_t kMaxPosition;
};


}  // namespace LightGBM


#endif   // LightGBM_METRIC_H_
