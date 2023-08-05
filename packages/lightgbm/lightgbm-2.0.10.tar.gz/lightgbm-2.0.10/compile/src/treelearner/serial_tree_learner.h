#ifndef LIGHTGBM_TREELEARNER_SERIAL_TREE_LEARNER_H_
#define LIGHTGBM_TREELEARNER_SERIAL_TREE_LEARNER_H_

#include <LightGBM/utils/random.h>
#include <LightGBM/utils/array_args.h>

#include <LightGBM/tree_learner.h>
#include <LightGBM/dataset.h>
#include <LightGBM/tree.h>

#include "feature_histogram.hpp"
#include "split_info.hpp"
#include "data_partition.hpp"
#include "leaf_splits.hpp"

#include <cstdio>
#include <vector>
#include <random>
#include <cmath>
#include <memory>
#ifdef USE_GPU
// Use 4KBytes aligned allocator for ordered gradients and ordered hessians when GPU is enabled.
// This is necessary to pin the two arrays in memory and make transferring faster.
#include <boost/align/aligned_allocator.hpp>
#endif

namespace LightGBM {

/*!
* \brief Used for learning a tree by single machine
*/
class SerialTreeLearner: public TreeLearner {
public:
  explicit SerialTreeLearner(const TreeConfig* tree_config);

  ~SerialTreeLearner();

  void Init(const Dataset* train_data, bool is_constant_hessian) override;

  void ResetTrainingData(const Dataset* train_data) override;

  void ResetConfig(const TreeConfig* tree_config) override;

  Tree* Train(const score_t* gradients, const score_t *hessians, bool is_constant_hessian) override;

  Tree* FitByExistingTree(const Tree* old_tree, const score_t* gradients, const score_t* hessians) const override;

  void SetBaggingData(const data_size_t* used_indices, data_size_t num_data) override {
    data_partition_->SetUsedDataIndices(used_indices, num_data);
  }

  void AddPredictionToScore(const Tree* tree, double* out_score) const override {
    if (tree->num_leaves() <= 1) { return; }
    CHECK(tree->num_leaves() <= data_partition_->num_leaves());
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < tree->num_leaves(); ++i) {
      double output = static_cast<double>(tree->LeafOutput(i));
      data_size_t cnt_leaf_data = 0;
      auto tmp_idx = data_partition_->GetIndexOnLeaf(i, &cnt_leaf_data);
      for (data_size_t j = 0; j < cnt_leaf_data; ++j) {
        out_score[tmp_idx[j]] += output;
      }
    }
  }

protected:
  /*!
  * \brief Some initial works before training
  */
  virtual void BeforeTrain();

  /*!
  * \brief Some initial works before FindBestSplit
  */
  virtual bool BeforeFindBestSplit(const Tree* tree, int left_leaf, int right_leaf);

  virtual void FindBestSplits();

  virtual void ConstructHistograms(const std::vector<int8_t>& is_feature_used, bool use_subtract);

  virtual void FindBestSplitsFromHistograms(const std::vector<int8_t>& is_feature_used, bool use_subtract);

  /*!
  * \brief Partition tree and data according best split.
  * \param tree Current tree, will be splitted on this function.
  * \param best_leaf The index of leaf that will be splitted.
  * \param left_leaf The index of left leaf after splitted.
  * \param right_leaf The index of right leaf after splitted.
  */
  virtual void Split(Tree* tree, int best_leaf, int* left_leaf, int* right_leaf);

  /*!
  * \brief Get the number of data in a leaf
  * \param leaf_idx The index of leaf
  * \return The number of data in the leaf_idx leaf
  */
  inline virtual data_size_t GetGlobalDataCountInLeaf(int leaf_idx) const;
  /*! \brief number of data */
  data_size_t num_data_;
  /*! \brief number of features */
  int num_features_;
  /*! \brief training data */
  const Dataset* train_data_;
  /*! \brief gradients of current iteration */
  const score_t* gradients_;
  /*! \brief hessians of current iteration */
  const score_t* hessians_;
  /*! \brief training data partition on leaves */
  std::unique_ptr<DataPartition> data_partition_;
  /*! \brief used for generate used features */
  Random random_;
  /*! \brief used for sub feature training, is_feature_used_[i] = false means don't used feature i */
  std::vector<int8_t> is_feature_used_;
  /*! \brief pointer to histograms array of parent of current leaves */
  FeatureHistogram* parent_leaf_histogram_array_;
  /*! \brief pointer to histograms array of smaller leaf */
  FeatureHistogram* smaller_leaf_histogram_array_;
  /*! \brief pointer to histograms array of larger leaf */
  FeatureHistogram* larger_leaf_histogram_array_;

  /*! \brief store best split points for all leaves */
  std::vector<SplitInfo> best_split_per_leaf_;

  /*! \brief stores best thresholds for all feature for smaller leaf */
  std::unique_ptr<LeafSplits> smaller_leaf_splits_;
  /*! \brief stores best thresholds for all feature for larger leaf */
  std::unique_ptr<LeafSplits> larger_leaf_splits_;

#ifdef USE_GPU
  /*! \brief gradients of current iteration, ordered for cache optimized, aligned to 4K page */
  std::vector<score_t, boost::alignment::aligned_allocator<score_t, 4096>> ordered_gradients_;
  /*! \brief hessians of current iteration, ordered for cache optimized, aligned to 4K page */
  std::vector<score_t, boost::alignment::aligned_allocator<score_t, 4096>> ordered_hessians_;
#else
  /*! \brief gradients of current iteration, ordered for cache optimized */
  std::vector<score_t> ordered_gradients_;
  /*! \brief hessians of current iteration, ordered for cache optimized */
  std::vector<score_t> ordered_hessians_;
#endif

  /*! \brief Store ordered bin */
  std::vector<std::unique_ptr<OrderedBin>> ordered_bins_;
  /*! \brief True if has ordered bin */
  bool has_ordered_bin_ = false;
  /*! \brief  is_data_in_leaf_[i] != 0 means i-th data is marked */
  std::vector<char> is_data_in_leaf_;
  /*! \brief used to cache historical histogram to speed up*/
  HistogramPool histogram_pool_;
  /*! \brief config of tree learner*/
  const TreeConfig* tree_config_;
  int num_threads_;
  std::vector<int> ordered_bin_indices_;
  bool is_constant_hessian_;
};

inline data_size_t SerialTreeLearner::GetGlobalDataCountInLeaf(int leafIdx) const {
  if (leafIdx >= 0) {
    return data_partition_->leaf_count(leafIdx);
  } else {
    return 0;
  }
}

}  // namespace LightGBM
#endif   // LightGBM_TREELEARNER_SERIAL_TREE_LEARNER_H_
