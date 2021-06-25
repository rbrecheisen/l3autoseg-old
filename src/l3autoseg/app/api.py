from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .backend import get_datasets


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def datasets(request):
    if request.method == 'GET':
        objects = get_datasets()
        dataset_ids = []
        for obj in objects:
            dataset_ids.append(obj.id)
        return Response({'dataset_ids': dataset_ids}, status=200)
    if request.method == 'POST':
        return Response({'dataset_id': 0}, status=201)
    return Response({}, status=404)
