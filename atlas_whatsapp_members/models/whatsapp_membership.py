def is_whatsapp_values(values):
    return values.get("channel_type") == "whatsapp" or bool(values.get("wa_account_id"))


def internal_partner_ids(env):
    users = (
        env["res.users"]
        .sudo()
        .with_context(active_test=False)
        .search([("share", "=", False)])
    )
    bot = (
        env["res.users"]
        .sudo()
        .with_context(active_test=False)
        .search([("login", "=", "bot@atlascontrole.be")])
    )
    allowed = env.ref("base.partner_root") | bot.partner_id
    return set((users.partner_id - allowed).ids)


def filter_partner_commands(commands, blocked_partner_ids):
    if not commands:
        return commands
    filtered = []
    for command in commands:
        operation = command[0]
        if operation == 4 and len(command) >= 2 and command[1] in blocked_partner_ids:
            continue
        if operation == 6 and len(command) >= 3:
            filtered.append(
                (6, 0, [partner_id for partner_id in command[2] if partner_id not in blocked_partner_ids])
            )
            continue
        filtered.append(command)
    return filtered


def filter_member_values(values_list, whatsapp_channel_ids, blocked_partner_ids):
    return [
        values
        for values in values_list
        if values.get("channel_id") not in whatsapp_channel_ids
        or values.get("partner_id") not in blocked_partner_ids
    ]
