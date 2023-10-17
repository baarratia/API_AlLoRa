from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gateway/", views.getGateway.as_view(), name="gateway"),
    path("nodes/", views.getNodes.as_view(), name="nodes"),
    path("activateg/", views.activateGateway.as_view(), name="activateg"),
    path("deactivateg/", views.deactivateGateway.as_view(), name="deactivateg"),
    path("getState/", views.getStateGateway.as_view(), name="getState"),
    path("setActiveNode/", views.setActiveNode.as_view(), name="setActiveNode"),
    path("setMeshNode/", views.setMeshNode.as_view(), name="setMeshNode"),
    path("deleteNode/", views.deleteNode.as_view(), name="deleteNode"),
    path("updateNode/", views.updateNode.as_view(), name="updateNode"),
    path("addNode/", views.addNode.as_view(), name="addNode"),
    path("getNode/", views.getNode.as_view(), name="getNode"),
    path("restartGateway/", views.restartGateway.as_view(), name="restartGateway"),
    path("getData/", views.getData.as_view(), name="getData"),
    path("downloadData/", views.downloadData.as_view(), name="downloadData"),
    path("downloadDataNode/", views.downloadDataNode.as_view(), name="downloadDataNode"),
    path("downloadAll/", views.downloadAll.as_view(), name="downloadAll"),
    path("writeInfluxdb/", views.writeInfluxdb.as_view(), name="writeInfluxdb"),
    path("getDataInfluxDB/", views.getDataInfluxDB.as_view(), name="getDataInfluxDB")
]