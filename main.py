import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_vcard(contact_data):
    """
    Creates a vCard QR code from contact data

    Parameters:
    - contact_data: Dictionary with name, surname, organization...

    Returns:
    - vCard data
    """
    vcard = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{contact_data.get('surname', '')};{contact_data.get('name', '')};",
        f"FN:{contact_data.get('name', '')} {contact_data.get('surname', '')}",
        f"ORG:{contact_data.get('organization', '')}",
    ]

    # Add optional fields if they exist
    if "email" in contact_data:
        vcard.append(f"EMAIL:{contact_data['email']}")
    if "phone" in contact_data:
        vcard.append(f"TEL:{contact_data['phone']}")
    if "title" in contact_data:
        vcard.append(f"TITLE:{contact_data['title']}")
    if "url" in contact_data:
        vcard.append(f"URL:{contact_data['url']}")

    vcard.append("END:VCARD")

    # Join all lines with proper line endings
    vcard_text = "\r\n".join(vcard)
    return vcard_text


def create_qr(vcard_data):
    """
    Creates a QR code image from vCard data

    Parameters:
    - vcard_data: String with vCard data

    Returns:
    - QR code image
    """
    qr = qrcode.QRCode(
        version=None,  # Automatically determine version
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=0,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    return qr_img

def load_font(name, size):
    """
    Loads a font from the specified path and size

    Parameters:
    - name: Path to the font file
    - size: Size of the font

    Returns:
    - Font object
    """
    try:
        return ImageFont.truetype(name, size)
    except IOError:
        return ImageFont.load_default()


def create_conference_card(contact_data):
    """
    Creates a conference card with name, organization, and QR code containing vCard data

    Parameters:
    - contact_data: Dictionary with name, surname, organization
    """
    # Define dimensions (we use mm converted to pixels at 300 DPI)
    MM_TO_PX = 11.811  # 300 DPI / 25.4 mm per inch
    card_width = int(85 * MM_TO_PX)
    card_height = int(64 * MM_TO_PX)
    qr_size = int(40 * MM_TO_PX)

    card = Image.new("RGB", (card_width, card_height), color="white")
    draw = ImageDraw.Draw(card)

    name_font = load_font("Arial.ttf", int(5.5 * MM_TO_PX))
    org_font = ImageFont.truetype("Arial.ttf", int(4 * MM_TO_PX))

    full_name = f"{contact_data['name']} {contact_data['surname']}".strip()

    organization = contact_data.get("organization", "")

    # Position name and organization text
    name_position = (card_width // 2, 40)

    org_position = (card_width // 2, 40 + 60)

    draw.text(name_position, full_name, fill=(0, 0, 0), font=name_font, anchor="mm")
    draw.text(org_position, organization, fill=(0, 0, 0), font=org_font, anchor="mm")

    # Generate QR code with vCard data
    vcard = create_vcard(contact_data)
    qr_img = create_qr(vcard)

    # Resize QR code
    qr_img = qr_img.resize((qr_size, qr_size))

    # Position for the QR code (right side, centered vertically)
    qr_position = ((card_width - qr_size) // 2, 40 + 60 + 60)
    card.paste(qr_img, qr_position)

    return card


if __name__ == "__main__":
    contact_data = {
        "name": "Federico",  # required
        "surname": "Mesa",  # required
        "organization": "Universidad de Sevilla",  # optional
        "email": "lmesa@upo.es",  # Optional
        "phone": "+34123456789",  # Optional
        "title": "Professor",  # Optional
        "url": "https://www.example.com",  # Optional
    }

    card = create_conference_card(contact_data)
    card.save("conference_card.png")
