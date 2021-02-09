import os
from subprocess import call

import pandas as pd
import numpy as np

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

from .models import BlockCateInfo, BlockInfo, MpoolCateInfo, MpoolInfo
from .serializers import BlockCateSerializer, BlockSerializer, MpoolCateSerializer, MpoolSerializer

from .models import TrainingBlockModel, TrainingResultModel, TrainTiggerModel
from .models import ForecastDataModel, ForecastResultModel, ForecastTiggerModel

from .serializers import TrainingBlockSerializer, TrainingResultSerializer, TrainTiggerSerializer
from .serializers import ForecastDataSerializer, ForecastResultSerializer, ForecastTiggerSerializer

from .train import Training
from .forecast import Forecastting
from .consts import ORIGINAL_DATA_FILE, ORIGINAL_TRAIN_DATA_FILE, TRAIN_RAW_RANG


class ForecastTiggerView(APIView):
    def get(self, request):
        """
        ForecastTiggerView
        """
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        ForecastTiggerView
        """

        quest_data = request.data

        print(quest_data)

        tmpfile = open(TRAIN_RAW_RANG, 'r')
        raw_range = tmpfile.read()
        tmpfile.close()

        print('raw_range: %s' % raw_range)

        if raw_range is None:
            raw_range = 508

        print('raw_range: %s' % raw_range)

        fore_obj = Forecastting()
        is_incrase, proba_positive, forecast_res = fore_obj.forecast(
            ORIGINAL_DATA_FILE, int(raw_range))

        print(is_incrase, proba_positive, forecast_res)
        print(type(forecast_res), type(proba_positive[0][0]),
              type(is_incrase[0]))

        is_pos = False
        if is_incrase[0] > 0:
            is_pos = True

        retest_set = TrainingBlockModel.objects.all().reverse()[:120]

        basefee_median_set = []
        for va_val in retest_set:
            basefee_median_set.append(va_val.parent_basefee)

        print(type(basefee_median_set))
        print(basefee_median_set)

        retest_median = np.median(basefee_median_set)

        s_set = ForecastResultSerializer(
            data={
                "epoch": quest_data.epoch,
                "parent_basefee": quest_data.basefee,
                "delta": forecast_res,
                "isPostive": is_pos,
                "delta_proba": proba_positive[0][0],
                "prodict_median": forecast_res + quest_data.basefee,
                "retest_median": retest_median,
            })

        print('s_set: %s' % s_set)
        print(s_set.is_valid())

        if s_set.is_valid():
            s_set.save()

        return Response(status=status.HTTP_200_OK)

class ForecastDataView(generics.ListCreateAPIView):
    """
    ForecastDataView
    """
    queryset = ForecastDataModel.objects.all()
    serializer_class = ForecastDataSerializer


class ForecastResultView(generics.ListCreateAPIView):
    """
    ForecastResultView
    """
    queryset = ForecastResultModel.objects.all()
    serializer_class = ForecastResultSerializer


class ForecastResultDetailView(generics.RetrieveAPIView):
    """
    ForecastResultDetailView
    """
    lookup_field = 'epoch'
    queryset = ForecastResultModel.objects.all()
    serializer_class = ForecastResultSerializer


# /////////////////////////////////////////////////////////////////////


class TrainingTiggerView(APIView):
    def get(self, request):
        """
        TrainningTiggerView get
        """
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        TrainningTiggerView post
        """
        print("train tigger")
        print(request)
        train_obj = Training()
        train_obj.train(ORIGINAL_DATA_FILE)
        return Response(status=status.HTTP_200_OK)


class TrainningDataView(generics.ListCreateAPIView):
    """
    TrainningView
    """
    queryset = TrainingBlockModel.objects.all()
    serializer_class = TrainingBlockSerializer

    def perform_create(self, serializer):
        serializer.save()

        # save to csv
        columns_title = [
            "epoch", "empty_num", "block_count", "parent_basefee",
            "count_block", "limit_total_block", "limit_avg_block",
            "cap_total_block", "cap_avg_block", "premium_total_block",
            "premium_avg_block", "range", "forecast"
        ]

        csv_file = []
        q_set = TrainingBlockModel.objects.all()
        for ele in q_set:
            tmp = [
                ele.epoch, ele.empty_num, ele.block_count, ele.parent_basefee,
                ele.count_block, ele.limit_total_block, ele.limit_avg_block,
                ele.cap_total_block, ele.cap_avg_block,
                ele.premium_total_block, ele.premium_avg_block, ele.backward, 0
            ]
            csv_file.append(tmp)

        df_i = pd.DataFrame(csv_file, columns=columns_title)
        df_i.to_csv(ORIGINAL_DATA_FILE, index=False)


class TrainingResultView(generics.ListCreateAPIView):
    """
    TrainingResultView
    """
    queryset = TrainingResultModel.objects.all()
    serializer_class = TrainingResultSerializer


class TrainingResultDetailView(generics.RetrieveAPIView):
    """
    TrainingResultDetailView
    """
    lookup_field = 'epoch'
    queryset = TrainingResultModel.objects.all()
    serializer_class = TrainingResultSerializer


# /////////////////////////////////////////////////////////////////////

# class Blockview(APIView):
#     """
#     Blockview
#     """

#     def get(self, request):
#         """
#         block view get method
#         """

#         q_set = BlockInfo.objects.all()
#         s_set = BlockSerializer(instance=q_set, many=True)
#         return Response(s_set.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """
#         block view post method
#         """

#         s_set = BlockSerializer(data=request.data)
#         if s_set.is_valid():
#             s_set.save()
#             return Response(data=s_set.data, status=status.HTTP_201_CREATED)
#         return Response(data=s_set.errors, status=status.HTTP_400_BAD_REQUEST)


class Blockview(generics.ListCreateAPIView):
    """
    Blockview
    """

    queryset = BlockInfo.objects.all()
    serializer_class = BlockSerializer


class BlockDeleteView(generics.DestroyAPIView):
    """
    BlockDeleteView
    """
    queryset = BlockInfo.objects.all()
    serializer_class = BlockSerializer


class BlockCateView(generics.ListCreateAPIView):
    """
    BlockCateView
    """

    queryset = BlockCateInfo.objects.all()
    serializer_class = BlockCateSerializer


class Mpoolview(generics.ListCreateAPIView):
    """
    Mpoolview
    """

    queryset = MpoolInfo.objects.all()
    serializer_class = MpoolSerializer


class MpoolCateView(generics.ListCreateAPIView):
    """
    MpoolCateView
    """

    queryset = MpoolCateInfo.objects.all()
    serializer_class = MpoolCateSerializer
