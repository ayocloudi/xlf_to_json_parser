# Sample XLIFF (XLF) content
xlf_content = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<xliff version=\"1.2\" xmlns=\"urn:oasis:names:tc:xliff:document:1.2\">
  <file source-language=\"en-US\" target-language=\"es-ES\" datatype=\"plaintext\" original=\"sample.xlf\">
    <body>
      <trans-unit id=\"1\" translate=\"yes\">
        <source>Hello, world!</source>
        <target>Hola, mundo!</target>
        <alt-trans match-quality=\"90\%\" origin=\"MT\">
          <target>Hola mundo!</target>
          <note>Machine Translation</note>
        </alt-trans>
      </trans-unit>
      <trans-unit id=\"2\" translate=\"yes\">
        <source>Good morning</source>
        <target>Buenos días</target>
        <alt-trans match-quality=\"85\%\" origin=\"TM\">
          <target>Buenos dias</target>
          <note>Translation Memory</note>
        </alt-trans>
      </trans-unit>
    </body>
  </file>
</xliff>"""

# Sample TBX content
tbx_content = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<tbx xmlns=\"urn:iso:std:iso:30042:ed-2\" style=\"dca\" type=\"TBX\">
  <body>
    <termEntry id=\"1\">
      <langSet xml:lang=\"en-US\">
        <tig>
          <term>Hello</term>
        </tig>
      </langSet>
      <langSet xml:lang=\"es-ES\">
        <tig>
          <term>Hola</term>
        </tig>
      </langSet>
    </termEntry>
    <termEntry id=\"2\">
      <langSet xml:lang=\"en-US\">
        <tig>
          <term>Good morning</term>
        </tig>
      </langSet>
      <langSet xml:lang=\"es-ES\">
        <tig>
          <term>Buenos días</term>
        </tig>
      </langSet>
    </termEntry>
  </body>
</tbx>"""

# Sample control.dat content
control_dat_content = """#BEGIN FILE
OriginalName=sample.xlf
sourceLanguage=en-US
targetLanguage=es-ES
Domain=GENERAL
Tool=SampleTool
#END FILE"""

# Save the sample files
with open('sample.xlf', 'w', encoding='utf-8') as xlf_file:
    xlf_file.write(xlf_content)

with open('sample.tbx', 'w', encoding='utf-8') as tbx_file:
    tbx_file.write(tbx_content)

with open('control.dat', 'w', encoding='utf-8') as control_file:
    control_file.write(control_dat_content)
