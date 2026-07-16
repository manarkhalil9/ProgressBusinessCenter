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

    # offices
    path("offices/", views.OfficeListView.as_view(), name="offices"),
    path("offices/<int:pk>/", views.OfficeDetailView.as_view(), name="office_detail"),

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

    # visit
    path('visit/', views.VisitCreateView.as_view(), name='visit'),
    path('visit/success/', views.visit_success, name='visit_success'),

    # referral
    path('referral/', views.ReferralCreateView.as_view(), name='referral'),
    path('referral/success/', views.referral_success, name='referral_success'),

    # business
    path('register/', views.BusinessRegistrationCreateView.as_view(), name='business_register'),
    path('register/success/',views.business_success, name='business_success'),

    # search bar
    path("search/", views.search, name="search"),

    # bookings
    path("book/<str:resource_type>/<int:pk>/", views.BookingCreateView.as_view(), name="book"),
    path("book/success/", views.booking_success, name="booking_success"),

    # dashboard
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('booking/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('booking/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking_cancel'),

    # auth
    path('accounts/signup/', views.signup, name='signup'),
]