# Mes modules Odoo custom

## `atlas_whatsapp_members` (#4009)

Bloque l’ajout des utilisateurs internes aux canaux WhatsApp, y compris lors
de la réponse d’un client à une facture. Le client, Nova
(`bot@atlascontrole.be`) et OdooBot restent membres. Les canaux de discussion
ordinaires ne sont pas filtrés.

Le module couvre les écritures de `discuss.channel.channel_partner_ids` et la
création de `discuss.channel.member`. Il ne retire aucun abonné des factures,
ne supprime aucun message et ne change pas `whatsapp.account.notify_user_ids`.

### Déploiement et recette

Ce dépôt ne déploie pas automatiquement le module et ne contient pas encore de
harnais de test Odoo. Le module ne doit pas être installé en production avant
d’avoir été vérifié sur un Odoo de recette.

1. Installer `atlas_whatsapp_members` sur la recette, avec le module
   `whatsapp` déjà présent.
2. Envoyer une facture WhatsApp à un contact de test, puis répondre depuis ce
   contact.
3. Vérifier que le message arrive dans Astro et que seuls le client et les bots
   autorisés sont membres du canal Odoo.
4. Vérifier que les abonnés de la facture et les invitations dans les canaux
   non WhatsApp sont inchangés.

Le cron quotidien #4009 reste nécessaire pour retirer les adhésions déjà
présentes. Ne le désactiver qu’après une recette réussie et une vérification
de l’absence de nouvelles adhésions internes.
