# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import CustomUser

# sign_up creates the User Sign Up view using the CustomUserCreationForm created in
# users/forms.py. 
def sign_up(request):
    #If the user submitted the form (i.e. 'POST')
    if request.method == 'POST':
        #then our form is our CustomUserCreationForm populated with the 
        #user's submitted data
        form = CustomUserCreationForm(request.POST)
        #if the form is valid (i.e. it passes all of the validations for 
        # each form field)
        if form.is_valid():
            #then save the form (but wait to commit it because we need
            # to set is_active to false for now so that the user can be 
            # confirmed via email)
            user = form.save(commit=False)
            #set is_active to false
            user.is_active = False
            #save the inactive user data
            user.save()
            #grab the domain name of our site to use in our email link
            current_site = get_current_site(request)
            #confirmation email subject
            subject = 'Activate Your PoPS Model Account'
            #create confirmation email message from our template and variables
            message = render_to_string('account_activation_email.html', {
                #get current user
                'user': user,
                #get current site domain
                'domain': current_site.domain,
                #create an encoded uid to use in the email confirmation link (
                # this encodes the user's primary key [user.pk]). When the user 
                # clicks on the link, this value gets passed to
                # the activate view and decoded to determine the user.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                # create a token to use in the email confirmation link. The
                # token is generated in users/tokens.py and is a combination
                # of the user's primary key and email_confirmed status. This
                # value is passed to activate view when user clicks on the link. 
                # After the email is confirmed, the activation link will no longer 
                # work because the token will no longer be valid.
                'token': account_activation_token.make_token(user),
            })
            #email the user using their provided email address
            user.email_user(subject, message)
            #redirect user to account_activation_sent view
            return redirect('account_activation_sent')
    #If the request method is not a POST (i.e. the user hasn't submitted data yet)
    else:
        #Then the form is our CustomUserCreationForm
        form = CustomUserCreationForm()
    #Return the signup form. If this is the first time it is rendered, it will be blank
    #If the user has already attempted to fill out the form, but it is invalid, then
    #the form will be populated with the user's content and error messages will be 
    #displayed
    return render(request, 'signup.html', {'form': form})

# Show user a page saying that the account_activation email has been sent
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html',)

# When the user clicks on the account_activation link in their email, this is the
# view that they are directed to. It passes the UID and token that was created in
# the sign_up view. 
def activate(request, uidb64, token):
    try:
        # The uidb64 is the user's primary key encoded using the secret key in settings. 
        # Try to decode it to get the user's pk.
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user using the decoded primary key.
        user = CustomUser.objects.get(pk=uid)
    # If we can't get the user from the decoded primary key, set user to none.
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # If the user exists (i.e. is not None), and the token for the user and
    # email_confirmed status checks out.
    if user is not None and account_activation_token.check_token(user, token):
        # Set user to active
        user.is_active = True
        # Set email_confirmed to true (this makes the token / email link no longer work)
        user.email_confirmed = True
        # Save the is_active and email_confirmed fields to the user object
        user.save()
        # Go ahead and log the user in
        login(request, user)
        # Redirect to the desired page
        return redirect('landing_page')
    #If the user and/or token do not work, direct the user to an invalid page
    else:
        return render(request, 'account_activation_invalid.html')