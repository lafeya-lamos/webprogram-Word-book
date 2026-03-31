"""错误时间模型迁移文件"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Слово'),
        ),
        migrations.CreateModel(
            name='WrongWordRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wrong_time', models.DateTimeField(auto_now_add=True, verbose_name='答错时间')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wrong_records', to='blog.article')),
            ],
        ),
    ]
