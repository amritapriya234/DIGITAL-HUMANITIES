import json
from lxml import etree

def create_tei_xml(metadata: dict, transcript_json_path: str, output_xml_path: str):
    """
    Combines Dublin Core metadata and JSON transcripts into a TEI-XML P5 document.
    """
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    # Namespaces
    TEI_NS = "http://www.tei-c.org/ns/1.0"
    DC_NS = "http://purl.org/dc/elements/1.1/"
    nsmap = {None: TEI_NS, "dc": DC_NS}

    # Root Element
    tei = etree.Element(f"{{{TEI_NS}}}TEI", nsmap=nsmap)

    # <teiHeader> Section
    teiHeader = etree.SubElement(tei, "teiHeader")
    fileDesc = etree.SubElement(teiHeader, "fileDesc")

    # Title & Metadata Statement
    titleStmt = etree.SubElement(fileDesc, "titleStmt")
    title = etree.SubElement(titleStmt, "title")
    title.text = metadata.get("title")

    respStmt = etree.SubElement(titleStmt, "respStmt")
    resp = etree.SubElement(respStmt, "resp")
    resp.text = "Digitized, transcribed, and encoded by"
    name = etree.SubElement(respStmt, "name")
    name.text = metadata.get("encoder")

    # Publication & Dublin Core Mapping inside teiHeader
    publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
    publisher = etree.SubElement(publicationStmt, "publisher")
    publisher.text = metadata.get("publisher")
    
    # Dublin Core Elements
    dc_title = etree.SubElement(publicationStmt, f"{{{DC_NS}}}title")
    dc_title.text = metadata.get("title")
    dc_creator = etree.SubElement(publicationStmt, f"{{{DC_NS}}}creator")
    dc_creator.text = metadata.get("interviewee")
    dc_date = etree.SubElement(publicationStmt, f"{{{DC_NS}}}date")
    dc_date.text = metadata.get("date")
    dc_subject = etree.SubElement(publicationStmt, f"{{{DC_NS}}}subject")
    dc_subject.text = metadata.get("subject_lcsh")

    # Source Description
    sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
    recordingStmt = etree.SubElement(sourceDesc, "recordingStmt")
    recording = etree.SubElement(recordingStmt, "recording", type="audio")
    media = etree.SubElement(recording, "media", mimeType="audio/wav", url=metadata.get("audio_url"))

    # <text> Body Section with Time-Synced Dialogue
    text_elem = etree.SubElement(tei, "text")
    body = etree.SubElement(text_elem, "body")
    div = etree.SubElement(body, "div", type="interview")

    for segment in transcript_data["segments"]:
        sp = etree.SubElement(div, "sp", who=f"#{metadata.get('speaker_id')}")
        speaker = etree.SubElement(sp, "speaker")
        speaker.text = metadata.get("interviewee")
        
        # Utterance with timecodes
        u = etree.SubElement(sp, "u", start=f"{segment['start']}s", end=f"{segment['end']}s")
        u.text = segment["text"]

    # Write TEI-XML to disk
    tree = etree.ElementTree(tei)
    tree.write(output_xml_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    print(f"Valid TEI-XML preservation file generated: {output_xml_path}")

if __name__ == "__main__":
    sample_metadata = {
        "title": "Oral History Interview with Margaret Vance",
        "interviewee": "Margaret Vance",
        "speaker_id": "vance_m_1942",
        "encoder": "Voices of the Archive Team",
        "publisher": "Community History Digital Archive",
        "date": "2026-10-15",
        "subject_lcsh": "Labor History -- Industrialization -- 20th Century",
        "audio_url": "http://localhost:8080/files/interview_101.wav"
    }
    
    create_tei_xml(
        metadata=sample_metadata,
        transcript_json_path="data/output/interview_101.json",
        output_xml_path="data/output/interview_101_preservation.xml"
    )