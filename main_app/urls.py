from django.urls import path
from . import views

urlpatterns = [

    # home
    path('', views.home, name='home'),

    # about
    path('about/', views.about, name='about'),

    # services
    path('services/', views.ServiceList.as_view(), name='services'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),

    # features
    path('features/', views.FeatureListView.as_view(), name='features'),
    path('features/<int:pk>/', views.FeatureDetailView.as_view(), name='feature_detail'),

    # branches
    path('branches/', views.BranchListView.as_view(), name='branches'),
    path('branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch_detail'),

    # rooms
    path('rooms/', views.MeetingRoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/', views.MeetingRoomDetailView.as_view(), name='room_detail'),

    # events
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),

    # gallery
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery_detail'),

    # faq
    path('faqs/', views.FAQListView.as_view(), name='faqs'),
    path('faqs/<int:pk>/', views.FAQDetailView.as_view(), name='faq_detail'),

    # contact
    path('contact/', views.ContactView.as_view(), name='contact'),

    # visit / referral
    path('visit/', views.VisitCreateView.as_view(), name='visit'),
    path('referral/', views.ReferralCreateView.as_view(), name='referral'),

    # business
    path('business/', views.BusinessDetailView.as_view(), name='business_detail'),

    # services actions
    path('business/add/<int:service_id>/', views.add_service, name='add_service'),
    path('business/remove/<int:service_id>/', views.remove_service, name='remove_service'),

    # auth
    path('accounts/signup/', views.signup, name='signup'),
]