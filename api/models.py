from django.db import models

class Lists(models.Model):
    id = models.CharField(max_length=36, primary_key=True)  # Use CharField for 'id' as text
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Use DateTimeField for 'created_at'
    name = models.CharField(max_length=100, null=True)  # Use CharField for 'name' as text
    owner_id = models.CharField(max_length=36)  # Use CharField for 'owner_id' as text

    class Meta:
        db_table = 'lists'  # Custom table name without app prefix
    def __str__(self):
        return self.name
    
class Todos(models.Model):
    id = models.CharField(max_length=36, primary_key=True)  # Use CharField for 'id' as text
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Use DateTimeField for 'created_at'
    completed_at = models.DateTimeField(null=True, blank=True)  # Use DateTimeField for 'completed_at'
    description = models.TextField(null=True)  # Use TextField for 'description' as text
    completed = models.BooleanField(default=False)  # Use BooleanField for 'completed'
    created_by = models.CharField(max_length=36, null=True)  # Use CharField for 'created_by' as text
    completed_by = models.CharField(max_length=36, null=True, blank=True)  # Use CharField for 'completed_by' as text
    list_id = models.CharField(max_length=36, null=True)

    class Meta:
        db_table = 'todos'  # Custom table name without app prefix
    def __str__(self):
        return self.description