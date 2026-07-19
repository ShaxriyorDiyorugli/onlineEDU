from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Category Name")
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategories",
        verbose_name="Parent Category"
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', verbose_name="Category")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taught_courses',
                                verbose_name="Teacher")
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    cover_image = models.ImageField(upload_to="courses/covers/", blank=True, null=True, verbose_name="Cover Image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'courses'
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Course")
    title = models.CharField(max_length=150,
                             verbose_name="Module Title")
    position = models.PositiveIntegerField(verbose_name="Module Position")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        db_table = 'modules'
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['position']


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="Module")
    title = models.CharField(max_length=150, verbose_name="Lesson Title")
    position = models.PositiveIntegerField(verbose_name="Lesson Position")

    video_url = models.URLField(null=True, blank=True, verbose_name="Video URL")
    content = models.TextField(null=True, blank=True, verbose_name="Text Content")
    attachment = models.FileField(upload_to="lessons/attachments/", null=True, blank=True, verbose_name="Attachment")

    def __str__(self):
        return f"{self.module.title} -> {self.title}"

    class Meta:
        db_table = 'lessons'
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ['position']