from django.db import models
"""
Models this application using
"""


class BlockInfo(models.Model):
    """
    block info of messages
    """
    epoch = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    block_count = models.IntegerField()
    basefee = models.BigIntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'blockinfo'
        managed = True
        ordering = ["epoch"]
        verbose_name = 'blockinfo'
        verbose_name_plural = 'blockinfos'


class BlockCateInfo(models.Model):
    """
    category info the different types of message info
    """
    epoch = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    cate_code = models.IntegerField()
    count = models.IntegerField()
    gas_limit_avg = models.BigIntegerField(null=True, blank=True)
    gas_limit_total = models.BigIntegerField(null=True, blank=True)
    gas_cap_avg = models.BigIntegerField(null=True, blank=True)
    gas_cap_total = models.BigIntegerField(null=True, blank=True)
    gas_premium_avg = models.BigIntegerField(null=True, blank=True)
    gas_premium_total = models.BigIntegerField(null=True, blank=True)
    value = models.BigIntegerField(null=True, blank=True)
    foreign = models.ForeignKey(BlockInfo,
                                related_name="cates",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        ordering = ["created"]


class MpoolInfo(models.Model):
    """
    mpool info of messages
    """
    created = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'mpoolinfo'
        managed = True
        ordering = ["epoch"]
        verbose_name = 'mpoolinfo'
        verbose_name_plural = 'mpoolinfos'


class MpoolCateInfo(models.Model):
    """
    category info the different types of message info
    """
    created = models.DateTimeField(auto_now_add=True)
    epoch = models.IntegerField()
    cate_code = models.IntegerField()
    count = models.IntegerField()
    gas_limit_avg = models.BigIntegerField(null=True, blank=True)
    gas_limit_total = models.BigIntegerField(null=True, blank=True)
    gas_cap_avg = models.BigIntegerField(null=True, blank=True)
    gas_cap_total = models.BigIntegerField(null=True, blank=True)
    gas_premium_avg = models.BigIntegerField(null=True, blank=True)
    gas_premium_total = models.BigIntegerField(null=True, blank=True)
    value = models.BigIntegerField(null=True, blank=True)
    foreign = models.ForeignKey(MpoolInfo,
                                related_name="cates",
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        ordering = ["created"]


# /////////////////////////////////////////////////////////////


class TrainingBlockModel(models.Model):
    epoch = models.IntegerField(unique=True)
    empty_num = models.IntegerField()
    block_count = models.IntegerField()
    parent_basefee = models.BigIntegerField()
    count_block = models.IntegerField()
    limit_total_block = models.BigIntegerField()
    limit_avg_block = models.BigIntegerField()
    cap_total_block = models.BigIntegerField()
    cap_avg_block = models.BigIntegerField()
    premium_total_block = models.BigIntegerField()
    premium_avg_block = models.BigIntegerField()
    backward = models.IntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'trainingBlock'
        managed = True
        verbose_name = 'TrainDataModel'
        verbose_name_plural = 'TrainDataModels'


class TrainingResultModel(models.Model):
    epoch = models.IntegerField(unique=True)
    parent_basefee = models.BigIntegerField()
    delta = models.BigIntegerField(default=0)
    isPostive = models.BooleanField(default=True)
    delta_proba = models.FloatField(default=0)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'trainResult'
        managed = True
        verbose_name = 'TrainResultModel'
        verbose_name_plural = 'TrainResultModels'


class TrainTiggerModel(models.Model):
    epoch = models.IntegerField(unique=True)
    isOk = models.BooleanField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'TrainTigger'
        managed = True
        verbose_name = 'TrainTiggerModel'
        verbose_name_plural = 'TrainTiggerModels'


# /////////////////////////////////////////////////////////////


class ForecastDataModel(models.Model):
    epoch = models.IntegerField(unique=True)
    empty_num = models.IntegerField()
    block_count = models.IntegerField()
    parent_basefee = models.BigIntegerField()
    count_block = models.IntegerField()
    limit_total_block = models.BigIntegerField()
    limit_avg_block = models.BigIntegerField()
    cap_total_block = models.BigIntegerField()
    cap_avg_block = models.BigIntegerField()
    premium_total_block = models.BigIntegerField()
    premium_avg_block = models.BigIntegerField()
    backward = models.IntegerField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'forecast_data'
        managed = True
        verbose_name = 'ForecastDataModel'
        verbose_name_plural = 'ForecastDataModels'


class ForecastResultModel(models.Model):
    epoch = models.IntegerField(unique=True)
    parent_basefee = models.BigIntegerField()
    delta = models.FloatField(default=0)
    isPostive = models.BooleanField(default=True)
    delta_proba = models.FloatField(default=0)

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'forecast_result'
        managed = True
        verbose_name = 'ForecastResultModel'
        verbose_name_plural = 'ForecastResultModels'


class ForecastTiggerModel(models.Model):
    epoch = models.IntegerField(unique=True)
    isOk = models.BooleanField()

    def __str__(self):
        return format(self.epoch)

    class Meta:
        db_table = 'ForecastTigger'
        managed = True
        verbose_name = 'ForecastTiggerModel'
        verbose_name_plural = 'ForecastTiggerModels'
