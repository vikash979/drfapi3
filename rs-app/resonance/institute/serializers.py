from rest_framework import serializers
from institute.models import Classs, Program, Target, Sessions, SessionProgram, Phase, Batch, CscDetails,Center

from subject.models import MasterSubject,Subject,TOC





class ClasssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classs
        fields = ('label','id',)
        

class MasterSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSubject
        fields = ('short_code','url')



class SubjectSerializer(serializers.ModelSerializer):
    #classs =ClasssSerializer(many=False)
    #master_subject = MasterSubjectSerializer(many=False)
    class Meta:
        model = Subject
        fields = ('description',)


class TOCSerializer(serializers.ModelSerializer):
	#subject = SubjectSerializer(many=False)
    parent = serializers.SerializerMethodField()


    class Meta:
        model = TOC
        fields = ('label','level','parent','subject','parent')
        depth = 1

    def get_parent(self,obj):
        print(obj.parent)        
        return TOCSerializer(obj.parent).data
        

	
		
		

	
    