from django.urls import path
from main.api.views import ProfileViewSet, AddContentViewSet, CreateLikeView, LikeViewSet, AddContentCreateView


urlpatterns = [
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve'})),
    path('profiles/', ProfileViewSet.as_view({'get': 'list'}), name='profiles'),
    path('profiles/update/', ProfileViewSet.as_view({'post': 'partial_update'}), name='update'),
    # path('profiles/updategeo/', ProfileViewSet.as_view({'post': 'update_geo'}), name='update_geo'),

    path('profiles/listcontent/', AddContentViewSet.as_view({'get': 'list'})),
    path('profiles/addcontent/', AddContentCreateView.as_view(), name='add_content'),
    # path('profiles/addcontent/', AddContentViewSet.as_view({'post': 'create'}), name='add_content'),

    # path('profiles/addlike/', CreateLikeView.as_view(), name='add_like'),
    path('profiles/addlike/', LikeViewSet.as_view({'post': 'create'}), name='add_like'),
]