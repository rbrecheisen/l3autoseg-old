from django.http import HttpResponse
from django.core.files import File
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ImageModel
from barbell2light.dicom import is_dicom_file


# ----------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def images(request):
    file_obj = request.FILES.get('file_obj', None)
    if file_obj is None:
        return Response({'message': 'Image file object missing'}, status=422)
    if not is_dicom_file(file_obj):
        return Response({'message': 'Image is not a DICOM'}, status=422)
    img = ImageModel.objects.create(file_obj=file_obj, file_name=file_obj.name, owner=request.user)
    return Response({'image_id': img.id, 'file_name': img.file_name}, status=201)


# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def image(request, image_id):
    img = ImageModel.objects.get(pk=image_id)
    if request.user == img.owner:
        if request.method == 'GET':
            with open(img.file_obj.path, 'rb') as ff:
                response = HttpResponse(File(ff), content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(img.file_name)
                return response
        elif request.method == 'DELETE':
            img.delete()
            return Response({}, status=200)
        else:
            pass
    else:
        return Response({'error': 'User is not owner'}, status=403)
