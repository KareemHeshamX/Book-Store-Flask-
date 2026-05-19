from extensions import db
from models import Book, User, Order, OrderItem


def seed_database():
    """Seed the database with sample data if tables are empty."""
    _seed_books()
    _seed_demo_user()


def _seed_books():
    """Insert sample books into an empty catalog."""
    if Book.query.count() > 0:
        return

    books_data = [
        {
            'title': 'The Architecture of Silence',
            'author': 'Julian Barnes',
            'price': 45.00,
            'category': 'Architecture',
            'book_format': 'Hardcover',
            'description': 'A masterful exploration of space, memory, and the unspoken language of structures.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuB7tRmXCArmaBZCdS-PkkVe3NXGbHTG9Tjat0WRiDSh4z0TrChwI7znP92NRRJ4KCjqt4k4Qrsy3JcZtLFnERfsGY2kulIKVRJ26nii1E5Y2zSJq1OX3tmN1hRgNhjsoH0c4fADn7mwaXOFKd11j3WjhP3cmOYtJN5m7ZnevX8KHNndSSED17K9D4ZVSHUKnX8u8cKngz0iGdOTLD6l4mbpa60Jw-yPZgaBVpn5AWx8_lflYomOXCxFai79ufkbL5Sx1nTska5kDtg'
        },
        {
            'title': 'Design as Art',
            'author': 'Bruno Munari',
            'price': 35.00,
            'category': 'Graphic Design',
            'book_format': 'Softcover',
            'description': 'A playful look at the visual arts, from advertising to industrial design.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCTCUntAQue90UvMMYfiBEP0uQ2E-lgerU0i7Sd830mLoYvhD5uKaKilB0Bn6k7fRfb1LwO4LrvHW2OdUca8SZX4iZ9oy0rV0I5midSbktfCG5VVOm7tcePCi00gWHvdLiN0NP4c6Ya9_t6Ibbvnfy6MlB3Hmmr9DfNynxjeV_yAGUYg9D8EMLluf1p1_N3tLIPyrprjwe5m_7axEFhzcZlsI_qM-wdCDz-9cl035A3IIqnpjuLrzMGzgR5C3ZanEpYqrhvGpu8m6Q'
        },
        {
            'title': 'The Poetics of Space',
            'author': 'Gaston Bachelard',
            'price': 28.00,
            'category': 'Architecture',
            'book_format': 'Softcover',
            'description': 'A philosophical examination of the spaces we inhabit and their intimate meanings.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuC7PlWXkCBzxQw1_P_Uonr48wXj8-cm0lDNDSi6Y-jtLkvbAQsih6cD7Soq-mx5I14j92s3VhbvGKJIXHgbf_zRS8ZVejCBrBTzGMjXGTkDpUWNp-LnVxHLNig2DhE3AatTSU1O4hfvcql1L5did8VxvRgQLdbgLV8sAl-0A_siAHxtIaXQSlFewGMdYlTTsokHIrbMK9RC6yO6lxyNrPWHuwLUCZyCt4ihXXoEmKyds-FYN-1dmOPg9XkgbcGFCi-cdIlwZuMUQsc'
        },
        {
            'title': 'On Typography',
            'author': 'Eric Gill',
            'price': 42.00,
            'category': 'Typography',
            'book_format': 'Hardcover',
            'description': 'A classic essay on the art and craft of letter design.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBTRzSLo8q7c5NlqxPDgGeEOWfF8W0RBDue_Dsepay_axyoVRMglTqddQNiLTdXLR9uirNUlC1WbIWB6sFRIEV7SlTcn4q6KMU7o2jUzoWb5f7_u2uUbnOriONJpk58bU3l1BCXjAt9jfx8EjwEyZOpEMCCVbYYvldkZdimPltj464O0xXXRfi09h9z7Ij-5YSVlIvkuOrrUTiBEpwhu8A_vHEvqR5CbOxYSp9aeCeVyYOeRYqEVo8yWxDJMn_ovpNrHTyPBOngk2I'
        },
        {
            'title': 'Brutalism Resurgent',
            'author': 'Alistair Vance',
            'price': 85.00,
            'category': 'Architecture',
            'book_format': 'Hardcover',
            'description': 'A definitive survey of the brutalist architectural movement in the 21st century.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAKm-iUpt2HEn2mBLsFEDma6sv6W-Mwkwzhw49tiN3BB6DTdzRdLCBL6YpOSkN_sK9yBOqvdzkl20tJhw9KDqaSWZIDbNCX-q7pNYoxjp46JI4wcOhf2utwzz6Y6msy8m-40jqFUdhhNhC9EeoaauFD-UQ4YwH3pLw_I1Dfd-TXpj0CFFM8tOzFziOYhVAXCqbC00QxTWeZlQCUfVPQrK7VHF2G20lA3rwV97r0yZx9QpKgcSZaoWpBToWDFNuT6puOS1hZvvmnO8A'
        },
        {
            'title': 'Grid Systems',
            'author': 'Josef Müller-Brockmann',
            'price': 45.00,
            'category': 'Graphic Design',
            'book_format': 'Hardcover',
            'description': 'The definitive guide to grid systems in graphic design.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA05Tee0cFV9xTEMHyc7YB8UvLg24GDqG8bCmL0Pjl2O0X7d5E74wGvtrFzO9j9a9ks1j9R_FJh1JNuDVtR_9j3jteavkcQRDl8yOygOeX-6fzWNFk2KfMKdjOVt5eTvsXgqWdgCGgaplgaO3WkIAgJ5dFLUnb3gLhRQyhy_Y__56dcUGbCR_msIoZK5SCMhyIGkokxOoDSGnOgxH9-t4WAipR9WR_Gbb0nN0B1gocez9KNjQSMrvj1WZBVwSbgxHwRlMpOqONXV_U'
        },
        {
            'title': 'Silent Spaces',
            'author': 'Elena Rostova',
            'price': 120.00,
            'category': 'Photography',
            'book_format': 'Limited Edition',
            'description': 'A photographic journey through abandoned sacred spaces around the world.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCyFW8boR_IPkPqASclGbYM5OavIbeRzvjvydjYQ7GFefdzw9K26x7HIW4L0NTXBacVJywFInbznJV7aRFYVVpR8WXC6kN6HedWoRXW5bzqC2b-zQFyyzJ5cLU8OEQYYM57cl7XNHbLjPahyTKh86zNIgsvKFAilCd5zHqU67ub3Rqm8BzltwUWasK_phuTpJZQbvZK1os8-xyeV6f9eiVFdku7e0jOUyr4qT_34ve_VUTJQm0VbgtCJaFNSk8tUJowJrDR_Ej4hGQ'
        },
        {
            'title': 'The Shape of Things',
            'author': 'Marcus Chen',
            'price': 65.00,
            'category': 'Typography',
            'book_format': 'Hardcover',
            'description': 'An exploration of form and meaning in typographic design.',
            'image_url': ''
        },
        {
            'title': 'Organic Forms',
            'author': 'Sarah Jenkins',
            'price': 90.00,
            'category': 'Contemporary Art',
            'book_format': 'Hardcover',
            'description': 'A survey of organic forms in contemporary art and sculpture.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA5OSBMfuMx7LRKJCip2tBzEAcS2nFgAhcWdLlFa_sUbtDdxcpKXlTCq0MzPsEMlS5VHeNphcklv1kcWr1U434A4paagPkjEVALvttJbkGyIAkFj9aosy2rnZuol-_49zIKvu9Dql7uPh_HBRV_w863KiG8HNf9dLiPmD39wdGJ6Atlt2vPBWuZTkN-yfFzip_64Uf7WJev7Kjfh-qBf1g-m7Ss9QWt_vnxyqfhVnDahTvQaprhKszg2LLyxc3qu1iHBnKNwQoYMxs'
        },
        {
            'title': 'The Architecture of Light',
            'author': 'James Crawford',
            'price': 65.00,
            'category': 'Architecture',
            'book_format': 'Hardcover',
            'description': 'How light shapes our experience of the built environment.',
            'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBupme-CZY3uMxh4MXttspRVmBNNfU8rM9JwbsKof7tJsdQf2zNDNoDIqXyTeV2Y4bCF16JtMxIEfyVvYyvX6psd16R6PBhSQcWLnBPI5SUbOcNmar3rtT18upv4qPvntpY1mTSwBG1asSkUuelrX6x6t1yUopmqGe1eDQCkR00lhXTtkWzQg58qTZZzqV6k4CypkX4clN-2Xz7AeT-OR7c4887hN9Ms7Fes5H_W41WZAxr-SDQRg2DIfoBzN7d0UIEbPebd2C17fo'
        },
    ]

    for bdata in books_data:
        db.session.add(Book(**bdata))
    db.session.commit()


def _seed_demo_user():
    """Create a demo admin user with sample orders."""
    if User.query.count() > 0:
        return

    demo_user = User(
        full_name='Kareem Hesham',
        username='kareem_hesham',
        email='kareem.hesham@example.com',
        member_since='2024',
        is_admin=True
    )
    demo_user.set_password('password123')
    db.session.add(demo_user)
    db.session.commit()

    # Sample orders
    order1 = Order(
        user_id=demo_user.id,
        order_number='#TBS-8921',
        date='Oct 12, 2023',
        total=142.00,
        status='Delivered'
    )
    db.session.add(order1)
    db.session.flush()
    db.session.add(OrderItem(order_id=order1.id, book_title='The Architecture of Silence', quantity=1, price=45.00))
    db.session.add(OrderItem(order_id=order1.id, book_title='Design as Art', quantity=1, price=35.00))

    order2 = Order(
        user_id=demo_user.id,
        order_number='#TBS-8105',
        date='Sep 04, 2023',
        total=85.50,
        status='Delivered'
    )
    db.session.add(order2)

    order3 = Order(
        user_id=demo_user.id,
        order_number='#TBS-7422',
        date='Jul 22, 2023',
        total=120.00,
        status='Returned'
    )
    db.session.add(order3)
    db.session.commit()
