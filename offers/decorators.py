from	django.http	import	HttpResponseBadRequest

def	ajax_required(f):
    def	wrap(request,*args,**kwargs):
        if	not	request.is_ajax():
            return	HttpResponseBadRequest()
