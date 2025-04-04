import textwrap

help_text = textwrap.dedent(
    """
        <b>Существующие команды</b>:
        
        <b>/get_currency</b> - получение курса валют, которые берутся с внешнего сервиса
        <b>/config</b> - получение конфига: все курсы (заданные вручную), расходы и т.д.
        <b>/get_users</b> - получение всех пользователей, кто пользовался калькулятором
        <b>set_config &lt;ключ&gt; &lt;значение&gt;</b> - изменение конфига
        <b>set_config mode &lt;auto/manual&gt;</b> - переключение между автоматическим и ручным режимом получения курса
    """
)