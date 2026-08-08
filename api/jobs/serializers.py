from jobs.models import Currency , Job , JobCategory , Application , Skill
from rest_framework import serializers

class CurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    code = serializers.CharField(max_length = 10)

    def create(self , validated_data):
        return Currency.objects.create(**validated_data)

    def update(self , instance , validated_data):
        instance.code = validated_data.get("code" , instance.code)
        instance.save()
        return instance

    def validate_code(self , value):
        if Currency.objects.filter(code__iexact = value).exists():
            raise serializers.ValidationError("This currency is already exists!")
        
class SkillSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 50)

    def create(self , validated_data):
        return Skill.objects.create(**validated_data)

    def update(self , instance , validated_data):
        instance.name = validated_data.get("name" , instance.name)
        instance.save()
        return instance

    def validate_name(self , value):
        if Skill.objects.filter(name__iexact = value).exists():
            raise serializers.ValidationError("This skill is already exists")

class JobCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(max_length = 100)
    parent = serializers.PrimaryKeyRelatedField(queryset = JobCategory.objects.all())

    def create(self , validated_data):
        return JobCategory.objects.create(**validated_data)

    def update(self , instance , validated_data):
        instance.title = validated_data.get("title" , instance.title)
        instance.parent = validated_data.get("parent" , instance.parent)
        instance.save()
        return instance

    def validate_title(self , value):
        queryset = JobCategory.objects.filter(title__iexact = value)

        if self.instance:
            queryset = queryset.exclude(id = self.instance.id)

        if queryset:
            raise serializers.ValidationError("Category with this title is already exists")
        return value
        
        