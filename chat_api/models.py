from django.db import models

# Create your models here.

class ChatResponse(models.Model):
    # Explanation of the code
    explanation = models.TextField()
    # Solution based on the code smell
    solution = models.TextField()
    # Updated code
    code =  models.TextField()

    class Meta:
        ordering = ['explanation']