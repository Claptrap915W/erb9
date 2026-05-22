from django.contrib import admin  # 引入 Django 後台管理模組
from django import forms          # 引入 Django 表單模組，用於自訂表單
from .models import Listing       # 引入本地專案的 Listing 模型 (資料庫結構)
from taggit.forms import TagWidget # 引入 taggit 套件的 TagWidget (標籤輸入元件)
# Register your models here.

# 1. 定義自訂表單類別
class ListingAdminForm(forms.ModelForm):
    class Meta:                  # 設定表單的元數據 (配置資訊)
        model = Listing          # 指定這個表單對應到 Listing 模型
        fields = '__all__'       # 包含模型中的所有欄位
        widgets = {              # 覆寫特定欄位的 HTML 顯示元件
            # 將 'services' 欄位改用 TagWidget 顯示
            # 這會讓輸入框變成可自動補全、用逗號分隔的標籤輸入介面
            'services': TagWidget(),
        }


# 2. 定義後台管理類別，控制 Listing 在後台的顯示與行為
class ListingAdmin(admin.ModelAdmin):
    # 設定列表頁面要顯示的欄位
    # 注意：'tag_list' 不是模型欄位，而是下面定義的一個自訂方法
    list_display = 'id', 'title', 'is_published', 'tag_list', 'list_date', "doctor"
    
    # 設定哪些欄位是可點擊的連結，點擊後會進入編輯頁面
    list_display_links = ('id', 'title')
    
    # 在右側加入篩選器，允許管理者依照 'doctor' (醫生) 或 'services' (標籤) 來篩選資料
    list_filter = ('doctor', "services")
    
    # 設定哪些欄位可以直接在列表頁面進行編輯 (不需要點進去每一筆資料)
    list_editable = ('is_published',)
    
    # 設定搜尋框的搜尋範圍
    # "services__name" 使用雙底線語法，允許搜尋關聯標籤表中的名稱
    search_fields = ('title', 'description', "services__slug", "doctor__name",)
    
    # 設定分頁，每頁最多顯示 25 筆資料
    list_per_page = 25

    # 3. 覆寫查詢集方法 (效能優化關鍵)
    def get_queryset(self, request):
        # super() 呼叫父類別的方法取得原始查詢集
        # prefetch_related("services") 會一次性抓取所有相關的標籤資料
        # 這可以避免「N+1 查詢問題」，大幅提升列表頁載入速度
        return super().get_queryset(request).prefetch_related("services")

    # 4. 自訂方法：用於在 list_display 中顯示標籤列表
    def tag_list(self, obj):
        # obj.services.all() 取得該筆 Listing 的所有標籤
        # [tag.name for tag in ...] 將標籤物件轉為名稱字串列表
        # ",".join(...) 將列表用逗號連成一個字串
        # or "No tags" 表示如果沒有標籤，則顯示 "No tags"
        return ", ".join([tag.name for tag in obj.services.all()]) or "No tags"
    
    # 設定該自訂欄位在列表頁標頭 (Column Header) 顯示的名稱
    tag_list.short_description = "Services"

# 將 Listing 模型與 ListingAdmin 類別註冊到 Django 管理後台
admin.site.register(Listing, ListingAdmin)