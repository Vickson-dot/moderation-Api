from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Message, ModerationResult
from detoxify import Detoxify

try:
    detoxify_model = Detoxify('original')
except Exception as e:
    print(f"Erreur Detoxify: {e}")
    detoxify_model = None


@receiver(post_save, sender=Message)
def analyze_message(sender, instance, created, **kwargs):
    if not created:
        return

    if not detoxify_model:
        print("Detoxify non disponible")
        instance.status = 'approved'
        instance.save(update_fields=['status'])
        return

    try:
        results = detoxify_model.predict(instance.content)
        thresholds = settings.MODERATION_THRESHOLDS

        category = 'safe'
        should_flag = False

        if results['toxicity'] > thresholds['toxicity']:
            category = 'toxic'
            should_flag = True
        elif results['obscene'] > thresholds['obscene']:
            category = 'obscene'
            should_flag = True
        elif results['threat'] > thresholds['threat']:
            category = 'threat'
            should_flag = True
        elif results['insult'] > thresholds['insult']:
            category = 'insult'
            should_flag = True
        elif results['severe_toxicity'] > thresholds['severe_toxicity']:
            category = 'hate'
            should_flag = True

        ModerationResult.objects.create(
            message=instance,
            toxicity=results['toxicity'],
            severe_toxicity=results['severe_toxicity'],
            obscene=results['obscene'],
            threat=results['threat'],
            insult=results['insult'],
            identity_attack=results['identity_attack'],
            category=category
        )

        if should_flag:
            instance.status = 'flagged'
        else:
            instance.status = 'approved'

        instance.save(update_fields=['status'])

        print(f"Message {instance.id}: {category} (toxicity: {results['toxicity']:.2f})")

    except Exception as e:
        print(f"Erreur analyse: {e}")
        instance.status = 'approved'
        instance.save(update_fields=['status'])