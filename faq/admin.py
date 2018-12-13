from django.contrib import admin
from .models import Question, Topic

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer', 'topic', 'status', 'helpful_yes', 'helpful_no', 'sort_order', 'created_by','created_on', 'updated_by','updated_on')

    def save_model(self, request, obj, form, change):
        # If the question is new update the created_by field.
        if not change:
            obj.created_by = request.user

        # Always update the updated_by field
        obj.updated_by = request.user

        return super(QuestionAdmin, self).save_model(request, obj, form, change)
        
admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)