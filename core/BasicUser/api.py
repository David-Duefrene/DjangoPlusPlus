"""API for detached head for the basic user module."""
# Django imports
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

# Django REST imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    ListAPIView, GenericAPIView

# Knox imports
from knox.models import AuthToken

# Project imports
from .models import BasicUser
from .serializers import BasicUserSerializer, LoginSerializer, \
    RegisterSerializer, ChangePasswordSerializer, EditSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password', 'new_password',
    ),
)


class UserAPI(RetrieveUpdateDestroyAPIView):
    """Retrieves, creates, updates and deletes a basic user.

    Allows user to retrieve, create, update, delete their own account.

    Attributes:
        serializer_class: Default serializer set to BasicUserSerializer.
        register_serializer: Register serializer set to RegisterSerializer.
        edit_serializer: Edit serializer set to EditSerializer.
        permissions: Default permissions, set to is authenticated.
        create_permission: Allows anyone to create a user.
        queryset: Sets all users by default

    Methods:
        get_permissions(self): Returns IsAuthenticated unless it's a POST
            method, then returns AllowAny.
        patch(self, request, *args, **kwargs): Allow an authenticated user to
            update their profile.
        post(self, request, *args, **kwargs): Creates a BasicUser.
        delete(self, request, *args, **kwargs): Deletes a BasicUser.

    """

    serializer_class = BasicUserSerializer
    register_serializer = RegisterSerializer
    edit_serializer = EditSerializer
    permissions = IsAuthenticated
    create_permission = AllowAny
    retrieve_profile_permission = AllowAny
    queryset = BasicUser.objects.all()

    def get_permissions(self):
        """Return proper permissions based on method.

        Allows anyone to create and retrieve users but requires authentication
        for everything else.
        """
        if self.request.method == 'POST':
            return (self.create_permission(),)
        if self.request.method == 'GET':
            return (self.retrieve_profile_permission(),)
        return (self.permissions(),)

    def patch(self, request, *args, **kwargs):
        """Allow a basic user to update their profile information.

        Allows a user to change their first and last name and email
        Requires authentication

        Request Data: JSON(string)
            first_name: User's first name
            last_name: User's last name
            email: User's email

        Response Data: JSON(string)
            first_name: User's new first name
            last_name: User's new last name
            email: User's new email
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
        """Create a Basic User.

        Allows a non-authenticated user to create an account.

        Request.data: JSON(string)
            username: The new users username
            password: The new users password
            email: The new users email optional
            first_name: The new users first name optional
            last name: The new users last name optional

        Returns Response: JSON(string)
            user(object): The user who just logged in
                username: The user's username
                email: The user's email
                first_name: The new users first name
                last name: The new users last name
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
                "user": self.serializer_class(
                    user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            })

        except KeyError as error:
            return Response({'Error': str(error) + ' cannot be None'})

    def delete(self, request, *args, **kwargs):
        """Delete a user, requires authentication.

        Allows a user to delete their own account. No body is expected but
        does require authentication.

        Returns Response: JSON(string)
            Success: Confirmst if the user has been deleted.
        """
        request.user.delete()
        return Response({'Success': 'User has been deleted'})


class ListUsersAPI(ListAPIView):
    """Retrieves a list of basic users.

    Allows anyone to retrieve a list of basic users.

    Attributes:
        queryset: Sets all users by default
        serializer_class: Default serializer set to BasicUserSerializer.
    """

    queryset = BasicUser.objects.all()
    serializer_class = BasicUserSerializer


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


class PasswordResetAPI(GenericAPIView):
    """Sends a password reset email.

    Allows a user to receive an email to reset their password.

    Attributes:
        serializer_class: default serializer is
        permission_classes: default permission is AllowAny

    Methods:
        post(self, request): Sends a password reset email to a user
    """

    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """Send a password reset email to a user.

        request.data: JSON(string)
            email: The user's email associated with the account

        Returns Response: JSON(string)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': 'Password reset e-mail has been sent.'})


class PasswordResetConfirmAPI(GenericAPIView):
    """Finish resetting user's password.

    Password reset e-mail link is confirmed, so this sets the user's password.

    Attributes:
        serializer_class: PasswordResetConfirmSerializer by default
        permission_classes: AllowAny by default

    Methods:
        post(self, request): Verifies token and updates user's password
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        """Over ridded to hide password from logs."""
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Verify token and updates user's password.

        URL kwargs: reset_password/confirm/<uidb64>/<token>/
            uidb64 - the unique user ID
            token: the token generated when requesting a password change

        request.data: JSON(string)
            new_password: the new password the user is changing to

        returns Response:
            detail: lets the user know the password has been reset
        """
        data = {
            'new_password': request.data['new_password'],
            'uid': self.kwargs['uidb64'],
            'token': self.kwargs['token'],
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Password has been reset with the new password.'},
        )
