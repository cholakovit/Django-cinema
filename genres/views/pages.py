from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from pydantic import ValidationError
from django.shortcuts import redirect
from genres.dto.dto import GenreCreate
from genres.forms import GenreForm
from genres.services.services import (
    create_genre, 
    get_genre, 
    list_genres_serialized, 
    parse_skip_limit,
    delete_genre
)
from utils.neo4j import node_to_json

def _form_to_payload(cleaned: dict[str, object]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in cleaned.items():
        if isinstance(value, str) and value.strip() == "":
            out[key] = None
        else:
            out[key] = value
    return out

class GenreCreatePageView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "genre_form.html",
            {"form": GenreForm(), "title": "Create Genre"},
        )

    def post(self, request):
        form = GenreForm(request.POST)
        if not form.is_valid(): # form is not valid, return the form with errors
            return render(
                request,
                "genre_form.html",
                {"form": form, "title": "Create Genre"},
            )
        try: # form is valid, create the genre
            dto = GenreCreate.model_validate(_form_to_payload(form.cleaned_data))
            created = create_genre(dto)
        except ValueError as e: # error creating the genre, return the form with errors
            form.add_error(None, str(e))
            return render(
                request,
                "genre_form.html",
                {"form": form, "title": "Create Genre"},
            )
        gid = str(created["id"]) if created else ""
        return redirect("genre_detail_page", genre_id=gid)

#------------------------------------------------------

class GenreDeletePageView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self._row = get_genre(kwargs["genre_id"])
        if not self._row:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, genre_id):
        return render(
            request,
            "genre_confirm_delete.html",
            {"genre": node_to_json(self._row), "genre_id": genre_id},
        )
    
    def post(self, request, genre_id):
        ok = delete_genre(genre_id)
        if not ok:
            raise Http404()
        return redirect("genre_list_page")

#------------------------------------------------------

class GenreListPageView(TemplateView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        skip, limit = parse_skip_limit(self.request.GET)
        ctx["genres"] = list_genres_serialized(skip, limit)
        return ctx


class GenreDetailPageView(View):
    def get(self, request, genre_id):
        row = get_genre(genre_id)
        if not row:
            raise Http404()
        return render(
            request,
            "detail.html",
            {"genre": node_to_json(row)},
        )
