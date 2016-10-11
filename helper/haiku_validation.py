def validate_haiku(haiku_list):
    template_values = {
        'stanza1': '',
        'stanza2': '',
        'stanza3': ''
        }

    form_valid = False
    template_values['stanza1_error'] = stanza_invalid(haiku_list[0], 5)
    template_values['stanza2_error'] = stanza_invalid(haiku_list[1], 7)
    template_values['stanza3_error'] = stanza_invalid(haiku_list[2], 5)

    if template_values['stanza1_error'] == "":
        template_values['stanza1'] = haiku_list[0]
    if template_values['stanza2_error'] == "":
        template_values['stanza2'] = haiku_list[1]
    if template_values['stanza3_error'] == "":
        template_values['stanza3'] = haiku_list[2]

    if template_values['stanza1_error'] == "" and template_values['stanza2_error'] == "" and template_values['stanza3_error'] == "":
        form_valid = True

    return form_valid, template_values


def stanza_invalid(stanza, syllable_count):
    # This will return '' if valid, and an error string if invalid:
    # HAIKU_ERROR['incomplete'] if it's empty
    # HAIKU_ERROR['syllables'] if syllables are 'wrong'
    if not stanza:
        return HAIKU_ERROR_MESSAGES['incomplete']
    else:
        return ""
