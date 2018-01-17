# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    #科室名
    dname = models.CharField(max_length=20)

class Patient(models.Model):
    pname = models.CharField(max_length=20)
    #身份证号
    idnum = models.CharField(max_length=20)
    P_sexual = models.IntegerField(null=True)
    P_page = models.IntegerField(null=True)
    phonenum = models.CharField(max_length=20, null=True)

class Staff(models.Model):
    user = models.OneToOneField(User)
    #工作证号
    idnum = models.CharField(max_length=20)
    sname = models.CharField(max_length=20)
    phonenum = models.CharField(max_length=20, null=True)
    department = models.ForeignKey(Department, null=True)

class Treatproject(models.Model):
    tname = models.CharField(max_length=20)
    #0：固定或活动；1：活动；2：固定
    type = models.IntegerField(default=1)

class Material(models.Model):
    mname = models.CharField(max_length=30)
     #0：固定或活动；1：活动；2：固定
    type = models.IntegerField(default=1)
     #对于活动义齿：1：支架；2：基托；3：人工牙
    pos = models.IntegerField(default=1)

class RPDVisit(models.Model):
    #病历号
    idnum = models.CharField(max_length=30)

    pid = models.ForeignKey(Patient)
    sid =  models.ForeignKey(Staff)
    department = models.ForeignKey(Department, null=True)
    #1：固定；2：活动
    type = models.IntegerField(default=1)
    #取模时间
    make_model_date = models.DateField(null=True)
    #接模时间
    get_model_date = models.DateField(null=True)
     #试支架时间
    try_cradled = models.DateField(null=True)
    #试蜡型时间
    try_paraffin = models.DateField(null=True)
    #试排牙时间
    try_teeth_arrange = models.DateField(null=True)
    #试桩时间
    try_stake = models.DateField(null=True)
    #试冠时间
    try_crown = models.DateField(null=True)
    #试基台时间
    try_base = models.DateField(null=True)
    #完成时间
    finish_date = models.DateField(null=True)
    #制作费
    fee = models.FloatField(null=True)
    #用金量
    gold_use = models.FloatField(null=True)
    #固定：预备体边缘；活动：模型边缘；1：清楚；2：不清楚
    model_edge = models.IntegerField(null=True)
    #咬合，1：稳；2：不稳
    occlusion_state = models.IntegerField(null=True)
    #牙合位记录，1：有；2：无
    occlusion_record = models.IntegerField(null=True)
    #牙体预备，1：够；2：不够
    teeth_pre = models.IntegerField(null=True)
    #发现问题
    problem = models.TextField(null=True)
    #处理方法
    solution = models.TextField(null=True)
    #初检人
    precheck = models.CharField(max_length=20,null=True)
    #初检日期
    precheck_date = models.DateField(null=True)
    #终检人
    finalcheck = models.CharField(max_length=20,null=True)
    #终检日期
    finalcheck_date = models.DateField(null=True)
    #比色
    color = models.CharField(max_length=20,null=True)
    #模型组制作人
    model_maker = models.CharField(max_length=20,null=True)
    #模型组质检员
    model_checker = models.CharField(max_length=20,null=True)
    #蜡型组制作人
    paraffin_maker = models.CharField(max_length=20,null=True)
    #蜡型组质检员
    paraffin_checker = models.CharField(max_length=20,null=True)
    #打磨组制作人
    burnish_maker = models.CharField(max_length=20,null=True)
    #打磨组质检员
    burnish_checker = models.CharField(max_length=20,null=True)
    #固定：烤瓷组制作人；活动：排牙组制作人
    china_arrange_makeer = models.CharField(max_length=20,null=True)
    #固定：烤瓷组质检员；活动：排牙组制作人
    china_arrange_checker = models.CharField(max_length=20, null=True)
    #修复材料
    material = models.ManyToManyField(Material)
    #修复项目
    project = models.ManyToManyField(Treatproject)
    #设计说明及要求
    design_explain = models.TextField(null=True)
    #顶点坐标列表
    quadraticTops = models.TextField(null=True)
    #连接体中空？
    conntype_hollow = models.BooleanField(default=False)
    #舌板？
    tongue_cover = models.BooleanField(default=False)
    #腭板？
    maxilla_cover = models.BooleanField(default=False)
    #上牙连接体中空部分边界点列表
    innerPathList = models.TextField(null=True)
    #上牙肯尼迪分类
    KennedyTop = models.IntegerField(null=True)
    #下牙肯尼迪分类
    KennedyBot = models.IntegerField(null=True)
    #上牙缺损序列
    teethlosslistTop = models.TextField(null=True)
    #下牙缺损序列
    teethlosslistBot = models.TextField(null=True)


class Tooth(models.Model):
    vid = models.ForeignKey(RPDVisit)
    # 表示牙齿的位置
    pos = models.IntegerField(null=True)
    # 0：未缺失；1：缺失；2：未长成
    tooth_lost = models.IntegerField(null=True)
    # 0：无基托；1：完整基托；2：只保留舌侧基托
    tooth_base = models.IntegerField(null=True)
    # 近远中舌颊侧四个位置上的卡环类型：0-无卡环，1-铸造全卡，2-铸造半卡，3-弯制全卡，4-弯制半卡
    tooth_clasp = models.IntegerField(null=True)
    # 0：无支托；1：近中支托；2：远中支托
    tooth_support = models.IntegerField(null=True)
    # 0：无腭板/舌板；1：有腭板/舌板
    tongue_blank = models.IntegerField(null=True)

class Remark(models.Model):
    vid = models.ForeignKey(RPDVisit)
    identy_index = models.CharField(max_length=30)
    left_top_pos = models.CharField(max_length=30)
    remark_pos = models.CharField(max_length=30)
    content = models.TextField
