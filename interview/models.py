from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from user.models import User


class Interview(models.Model):
    title = models.CharField(max_length=128, verbose_name='제목')
    interviewee = models.CharField(max_length=128, verbose_name='인터뷰 대상자')
    interviewer = models.CharField(max_length=128, verbose_name='인터뷰어')
    photographer = models.CharField(max_length=128, verbose_name='포토그래퍼')
    content = models.TextField(verbose_name='내용')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    likes = models.ManyToManyField(User, related_name="likes", blank=True, verbose_name='공감수')
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')
    image = ProcessedImageField(
        upload_to='',
        processors=[ResizeToFit(width=960, upscale=False)],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    class Meta:
        db_table = '인터뷰'
        verbose_name = '인터뷰'
        verbose_name_plural = '인터뷰'
        permissions = [
            ('can_write_interview', 'Can Write Interview')
        ]


class Comment(models.Model):
    writer = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False, blank=False, verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    interview = models.ForeignKey(Interview, null=True, blank=True, on_delete=models.CASCADE, verbose_name='인터뷰')
    content = models.TextField(verbose_name='댓글 입력')

    def __str__(self):
        return self.content

    class Meta:
        db_table = '댓글'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
