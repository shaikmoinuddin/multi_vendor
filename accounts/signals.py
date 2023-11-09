from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


# signals
# emthod_2
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User is created successfully")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #create the user profile if not created
            UserProfile.objects.create(user=instance)
            print("profile does not exits, but created successfully")
        print("User is updated successfully")
    

# method_1
#post_save.connect(post_save_create_profile_receiver, sender=User)

# pre_save
@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    #print(instance.username, "the User is being saved")
    pass
    