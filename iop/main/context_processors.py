# Kontekst do wyciągania czy uzytkownik sie zweryfikował i jego adres email 
def verify_banner(request):
    return {
        'show_verify_banner': request.session.get('show_verify_banner', False),
        'verify_email': request.session.get('verify_email', '')
    }