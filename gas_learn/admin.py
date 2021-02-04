from django.contrib import admin
from .models import BlockInfo, BlockCateInfo, MpoolInfo, MpoolCateInfo
from .models import TrainingBlockModel, TrainingResultModel, TrainTiggerModel
from .models import ForecastDataModel, ForecastResultModel, ForecastTiggerModel

# Register your models here.


@admin.register(BlockInfo)
class BlockInfoAdmin(admin.ModelAdmin):
    list_display = ("block_count", "basefee", "epoch", "created")
    search_fields = list_display
    list_filter = list_display


@admin.register(BlockCateInfo)
class BlockCateInfoAdmin(admin.ModelAdmin):
    list_display = ("cate_code", "count", "epoch")
    search_fields = list_display
    list_filter = list_display


@admin.register(MpoolInfo)
class MpoolInfoAdmin(admin.ModelAdmin):
    list_display = ("created", "epoch")
    search_fields = list_display
    list_filter = list_display


@admin.register(MpoolCateInfo)
class MpoolCateInfoAdmin(admin.ModelAdmin):
    list_display = ("cate_code", "count")
    search_fields = list_display
    list_filter = list_display


# /////////////////////////////////////////////////////


@admin.register(TrainingBlockModel)
class TrainingBlockModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "empty_num", "block_count", "parent_basefee",
                    "count_block", "limit_total_block", "limit_avg_block",
                    "cap_total_block", "cap_avg_block", "premium_total_block",
                    "premium_avg_block")
    search_fields = ("epoch", "block_count")
    list_filter = ("block_count",)


@admin.register(TrainingResultModel)
class TrainingResultModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "parent_basefee")
    search_fields = list_display
    list_filter = search_fields


@admin.register(TrainTiggerModel)
class TrainTiggerModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "isOk")
    search_fields = list_display
    list_filter = search_fields


# ////////////////////////////////////////////////////


@admin.register(ForecastDataModel)
class ForecastDataModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "empty_num", "block_count", "parent_basefee",
                    "count_block", "limit_total_block", "limit_avg_block",
                    "cap_total_block", "cap_avg_block", "premium_total_block",
                    "premium_avg_block")
    search_fields = ("epoch", "block_count")
    list_filter = search_fields


@admin.register(ForecastResultModel)
class ForecastResultModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "parent_basefee", "delta", "isPostive", "delta_proba")
    search_fields = list_display
    list_filter = ("isPostive",)


@admin.register(ForecastTiggerModel)
class ForecastTiggerModelAdmin(admin.ModelAdmin):
    list_display = ("epoch", "isOk")
    search_fields = list_display
    list_filter = search_fields
