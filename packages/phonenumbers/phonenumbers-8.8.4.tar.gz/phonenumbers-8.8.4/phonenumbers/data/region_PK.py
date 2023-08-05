"""Auto-generated file, do not edit by hand. PK metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_PK = PhoneMetadata(id='PK', country_code=92, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{8}|[2-8]\\d{5,11}|9(?:[013-9]\\d{4,9}|2\\d(?:111\\d{6}|\\d{3,7}))', possible_length=(8, 9, 10, 11, 12), possible_length_local_only=(6, 7, 8)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:21|42)[2-9]\\d{7}|(?:2[25]|4[0146-9]|5[1-35-7]|6[1-8]|7[14]|8[16]|91)[2-9]\\d{6}|(?:2(?:3[2358]|4[2-4]|9[2-8])|45[3479]|54[2-467]|60[468]|72[236]|8(?:2[2-689]|3[23578]|4[3478]|5[2356])|9(?:2[2-8]|3[27-9]|4[2-6]|6[3569]|9[25-8]))[2-9]\\d{5,6}|58[126]\\d{7}', example_number='2123456789', possible_length=(9, 10), possible_length_local_only=(6, 7, 8)),
    mobile=PhoneNumberDesc(national_number_pattern='3(?:[014]\\d|2[0-5]|3[0-7]|55|64)\\d{7}', example_number='3012345678', possible_length=(10,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{5}', example_number='80012345', possible_length=(8,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='900\\d{5}', example_number='90012345', possible_length=(8,)),
    personal_number=PhoneNumberDesc(national_number_pattern='122\\d{6}', example_number='122044444', possible_length=(9,)),
    uan=PhoneNumberDesc(national_number_pattern='(?:2(?:[125]|3[2358]|4[2-4]|9[2-8])|4(?:[0-246-9]|5[3479])|5(?:[1-35-7]|4[2-467])|6(?:[1-8]|0[468])|7(?:[14]|2[236])|8(?:[16]|2[2-689]|3[23578]|4[3478]|5[2356])|9(?:1|22|3[27-9]|4[2-6]|6[3569]|9[2-7]))111\\d{6}', example_number='21111825888', possible_length=(11, 12)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='([89]00)(\\d{3})(\\d{2})', format='\\1 \\2 \\3', leading_digits_pattern=['[89]00'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(1\\d{3})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['1'], national_prefix_formatting_rule='\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{7,8})', format='\\1 \\2', leading_digits_pattern=['(?:2[125]|4[0-246-9]|5[1-35-7]|6[1-8]|7[14]|8[16]|91)[2-9]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{3})(\\d{6,7})', format='\\1 \\2', leading_digits_pattern=['2[349]|45|54|60|72|8[2-5]|9[2-469]', '(?:2[349]|45|54|60|72|8[2-5]|9[2-469])\\d[2-9]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(58\\d{3})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['58[126]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(3\\d{2})(\\d{7})', format='\\1 \\2', leading_digits_pattern=['3'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(111)(\\d{3})(\\d{3})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['(?:2[125]|4[0-246-9]|5[1-35-7]|6[1-8]|7[14]|8[16]|91)1', '(?:2[125]|4[0-246-9]|5[1-35-7]|6[1-8]|7[14]|8[16]|91)11', '(?:2[125]|4[0-246-9]|5[1-35-7]|6[1-8]|7[14]|8[16]|91)111'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{3})(111)(\\d{3})(\\d{3})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['2[349]|45|54|60|72|8[2-5]|9[2-9]', '(?:2[349]|45|54|60|72|8[2-5]|9[2-9])\\d1', '(?:2[349]|45|54|60|72|8[2-5]|9[2-9])\\d11', '(?:2[349]|45|54|60|72|8[2-5]|9[2-9])\\d111'], national_prefix_formatting_rule='(0\\1)')],
    mobile_number_portable_region=True)
