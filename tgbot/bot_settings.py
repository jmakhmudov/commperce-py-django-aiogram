import os

from elasticsearch import Elasticsearch

from app.models import AddPublication, Admin, Group, Settings

elastic = Elasticsearch([os.environ.get("ELASTICSEARCH_HOSTS")])

elastic_params = {
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "custom_analyzer",
                "search_analyzer": "custom_analyzer",
            }
        }
    },
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "tokenizer": "my_tokenizer",
                    "filter": [
                        "lowercase",
                        "russian_morphology",
                        "english_morphology",
                    ],
                }
            },
            "tokenizer": {
                "my_tokenizer": {"type": "pattern", "pattern": "[,;\\.\\s]+"}
            },
        }
    },
}


def get_active_settings(id=None):
    if id:
        id = str(id)
    settings = Settings.objects.filter(group__tgid=id)
    if settings.exists():
        return settings.first()
    return Settings.objects.filter(base=True).first()


API_TOKEN = os.environ.get("API_TOKEN")

ALLOWED_GROUPS = Group.objects.all()

ADMINS = Admin.objects.all()


async def check_publications():
    return AddPublication.objects.all()
