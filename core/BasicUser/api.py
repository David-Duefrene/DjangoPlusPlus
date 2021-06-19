"""API for detached head for the basic user module."""
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from knox.models import AuthToken

from .serializers import BasicUserSerializer, LoginSerializer, \
    RegisterSerializer, ChangePasswordSerializer, EditSerializer


class UserAPI(RetrieveUpdateDestroyAPIView):
    """Retrieves, creates, updates and deletes a basic user.

    Allows user to retrieve, create, update, delete their own account.

    Attributes:
        serializer: Default serializer.
        register_serializer: Serializer to register a user.
        edit_serializer: Serializer to Edit a user.
        permissions: Default permissions.
        create_permission: Permissions for creating a user.

    Methods:
        get_permissions(self): Returns IsAuthenticated unless it's a POST
            method, then returns AllowAny.
        patch(self, request, *args, **kwargs): Allow an authenticated user to
            update their profile.
        create(self, request, *args, **kwargs): Creates a BaseUser.

    """

    serializer_class = BasicUserSerializer
    register_serializer = RegisterSerializer
    edit_serializer = EditSerializer
    permissions = IsAuthenticated
    create_permission = AllowAny

    def get_permissions(self):
        """Return allow anyone to POST but require auth for everything else."""
        if self.request.method == 'POST':
            return (self.create_permission(),)
        return (self.permissions(),)

    def patch(self, request, *args, **kwargs):
        """Allow a basic user to update their profile information.

        Allows a user to change their first and last name and email
        Requires authentication

        Request Data: JSON(string)
            first_name: User's first name
            last_name: User's last name
            email: User's email
        """
        try:
            instance = request.user
            instance.first_name = request.data['first_name']
            instance.last_name = request.data['last_name']
            instance.email = request.data['email']
            instance.save()

            serializer = self.edit_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_update(serializer)
            return Response(serializer.data)

        except KeyError as error:
            return Response({'Error': str(error) + ' cannot be None'})

    def post(self, request, *args, **kwargs):
        """Create an Basic User.

        Allows a non-authenticated user to create an account

        Request.data: JSON(string)
            username: The new users username
            password: The new users password
            email: The new users email optional
            first_name: The new users first_name optional
            last name: The new users last name optional

        Returns Response: JSON(string)
            user(object): The user who just logged in
                username: The user's username
                email: The user's email
                first_name: The new users first_name optional
                last name: The new users last name optional
                get_absolute_url: The url to edit the user
            token: The new user's authentication token
        """
        try:
            if request.data['password'] is not None:
                hashed_pass = make_password(request.data['password'])
                request.data['password'] = hashed_pass

            serializer = self.register_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                "user": self.serializer(
                    user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            })

        except KeyError as error:
            return Response({'Error': str(error) + ' cannot be None'})


@api_view(['POST'])
def LoginAPI(request):
    """Log a already registered user in.

    Request Data: JSON(string)
        username: The user's username
        password: The user's password

    Returns Response:
        user(object): The user who just logged in
            username: The user's username
            email: The user's email
            first_name: The new users first_name optional
            last name: The new users last name optional
            get_absolute_url: The url to edit the user
    """
    serialzer = LoginSerializer(data=request.data)
    serialzer.is_valid(raise_exception=True)
    user = serialzer.validated_data

    return Response({
        "user": user.username,
        "token": AuthToken.objects.create(user)[1]
    })


@api_view(['PUT'])
@login_required
def ChangePasswordAPI(request):
    """Allow a user to update their password if they know their old one.

    Request Data: JSON(string)
        old_password: The user's old password
        new_password: The user's new password

    Response Data: JSON(string)
        status: The status of the request
        code: The response code for the request
        message: A more detailed generic status message
    """
    obj = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        # Check old password
        if not obj.check_password(serializer.data.get('old_password')):
            return Response({'old_password': ['Wrong password.']},
                            status=status.HTTP_400_BAD_REQUEST)
            pass

        # set_password also hashes the password that the user will get
        obj.set_password(serializer.data.get('new_password'))
        obj.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
        }

        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, token, *args, **kwargs):
    """Send an email to a user when they try and reset their password."""
    email_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'),
        token.key
    )

    send_mail(
        "Password Reset for {title}".format(title="News"),  # title
        email_message,  # message
        "noreply@somehost.local",  # from
        [token.user.email],  # to
    )
