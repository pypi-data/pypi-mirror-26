#include <LightGBM/prediction_early_stop.h>
#include <LightGBM/utils/log.h>

#include <algorithm>
#include <vector>
#include <cmath>
#include <limits>

namespace {

using namespace LightGBM;

PredictionEarlyStopInstance CreateNone(const PredictionEarlyStopConfig&) {
  return PredictionEarlyStopInstance{
    [](const double*, int) {
    return false;
  },
    std::numeric_limits<int>::max() // make sure the lambda is almost never called
  };
}

PredictionEarlyStopInstance CreateMulticlass(const PredictionEarlyStopConfig& config) {
  // margin_threshold will be captured by value
  const double margin_threshold = config.margin_threshold;

  return PredictionEarlyStopInstance{
    [margin_threshold](const double* pred, int sz) {
    if (sz < 2) {
      Log::Fatal("Multiclass early stopping needs predictions to be of length two or larger");
    }

    // copy and sort
    std::vector<double> votes(static_cast<size_t>(sz));
    for (int i = 0; i < sz; ++i) {
      votes[i] = pred[i];
    }
    std::partial_sort(votes.begin(), votes.begin() + 2, votes.end(), std::greater<double>());

    const auto margin = votes[0] - votes[1];

    if (margin > margin_threshold) {
      return true;
    }

    return false;
  },
    config.round_period
  };
}

PredictionEarlyStopInstance CreateBinary(const PredictionEarlyStopConfig& config) {
  // margin_threshold will be captured by value
  const double margin_threshold = config.margin_threshold;

  return PredictionEarlyStopInstance{
    [margin_threshold](const double* pred, int sz) {
    if (sz != 1) {
      Log::Fatal("Binary early stopping needs predictions to be of length one");
    }
    const auto margin = 2.0 * fabs(pred[0]);

    if (margin > margin_threshold) {
      return true;
    }

    return false;
  },
    config.round_period
  };
}

}

namespace LightGBM {

PredictionEarlyStopInstance CreatePredictionEarlyStopInstance(const std::string& type,
                                                              const PredictionEarlyStopConfig& config) {
  if (type == "none") {
    return CreateNone(config);
  } else if (type == "multiclass") {
    return CreateMulticlass(config);
  } else if (type == "binary") {
    return CreateBinary(config);
  } else {
    throw std::runtime_error("Unknown early stopping type: " + type);
  }
}

}
