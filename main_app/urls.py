from django.urls import path
from . import views

urlpatterns = [
    # home
    path('', views.home, name='home'),

    # about
    path('about/', views.about, name='about'),

    # services
    path('services/', views.ServiceList.as_view(), name='services_index'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # features
    path('features/', views.FeatureListView.as_view(), name='features'),
    path('features/<int:pk>/', views.FeatureDetailView.as_view(), name='feature_detail'),
    path('features/create/', views.FeatureCreateView.as_view(), name='feature_create'),
    path('features/<int:pk>/update/', views.FeatureUpdateView.as_view(), name='feature_update'),
    path('features/<int:pk>/delete/', views.FeatureDeleteView.as_view(), name='feature_delete'),

    # branches
    path('branches/', views.BranchListView.as_view(), name='branches'),
    path('branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch_detail'),
    path('branches/create/', views.BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/update/', views.BranchUpdateView.as_view(), name='branch_update'),
    path('branches/<int:pk>/delete/', views.BranchDeleteView.as_view(), name='branch_delete'),

    # meeting rooms
    path('rooms/', views.MeetingRoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.MeetingRoomDetailView.as_view(), name='room_detail'),
    path('rooms/create/', views.MeetingRoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/update/', views.MeetingRoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', views.MeetingRoomDeleteView.as_view(), name='room_delete'),

    # events
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # gallery
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery_detail'),

    # FAQ
    path('faqs/', views.FAQListView.as_view(), name='faqs'),
    path('faqs/<int:pk>/', views.FAQDetailView.as_view(), name='faq_detail'),

    # contact
    path('contact/', views.ContactCreateView.as_view(), name='contact'),

    # visits
    path('visit/', views.VisitCreateView.as_view(), name='visit'),

    # business registrations
    path('business/', views.BusinessListView.as_view(), name='businesses'),
    path('business/<int:pk>/', views.BusinessDetailView.as_view(), name='business_detail'),

    # many to many actions
    path('business/<int:business_id>/add_service/<int:service_id>/', views.add_service, name='add_service'),
    path('business/<int:business_id>/remove_service/<int:service_id>/', views.remove_service, name='remove_service'),

    # referral
    path('referral/', views.ReferralCreateView.as_view(), name='referral'),

    # signup
    path('accounts/signup', views.signup, name='signup'),
]