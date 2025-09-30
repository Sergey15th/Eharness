from django.db import models

from django.db import models
from freppledb.common.models import User
# Use the function "_" for all strings that need translation.
from django.utils.translation import gettext_lazy as _

# A subclass of AuditModel will inherit an field "last_modified" and "source".
from freppledb.common.models import HierarchyModel, AuditModel, Parameter

alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class UserCodes(AuditModel):
    user = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="User",
        db_comment="User",
        ) 
    code = models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        verbose_name = "User passcard"
        verbose_name_plural = "Users passcards"
        db_table = "users_passcards"

class CodesTypes(AuditModel):
    type = models.CharField(max_length=50, blank=False, null=False)
    pattern = models.CharField(max_length=100, blank=False, null=False)
    class Meta:
        verbose_name = "Code types"
        verbose_name_plural = "Codes types"
        db_table = "codes_types"

class LastUsedQR(AuditModel):
    def to_base62(self, num):
        """Перевод числа в 62-ричную систему"""
        if num == 0:
            return alphabet[0]
        base62 = []
        base = len(alphabet)
        while num > 0:
            num, rem = divmod(num, base)
            base62.append(alphabet[rem])
        return ''.join(reversed(base62)).zfill(4)
    def from_base62(self, s):
        """Перевод из 62-ричной системы в десятичную"""
        base = len(alphabet)
        num = 0
        for char in s:
            num = num * base + alphabet.index(char)
        return num    
    def _next_id(self) -> str:
        if not self.qr:
            return self.to_base62(0)
        else:
            return self.to_base62(num=self.from_base62(self.qr) + 1)
    model = models.CharField(primary_key=True, max_length=50, blank=False, null=False)
    qr = models.CharField(max_length=8, blank=False, null=False)
    class Meta:
        verbose_name = "Last used mQR"
        verbose_name_plural = "Last used mQRs"
        db_table = "last_qr"

class CodeScanEvent(AuditModel):
    session_id = models.CharField(max_length=150, blank=False, null=True)
    scan_data = models.CharField()  # Будет хранить массив с объектами нажатий
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="User",
        related_name="event_users",
        db_comment="User",
        )
    class Meta:
        verbose_name = "Code scan record"
        verbose_name_plural = "Codes scan records"
        db_table = "codes_scan_records"

    def __str__(self):
        return f"Session {self.session_id} - {len(self.scan_data)} keys"
    
    extra_dependencies = [
        Parameter,
    ]

    class Meta(AuditModel.Meta):
        db_table = "codescanevent"
        verbose_name = _("Code scan Event")
        verbose_name_plural = _("Code scan Events")
        ordering = ["created_at"]

from django.db import models

class Workstation(AuditModel):
    name = models.CharField(max_length=100, primary_key=True, verbose_name="Название")
    short_name = models.CharField(max_length=10, verbose_name="РМ", blank=True, null=True)
    image = models.ImageField(upload_to='img/', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    qr = models.TextField(blank=False, verbose_name="qr код")
    def __str__(self):
        return self.short_name