import os, sys, uuid, json

os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('SECRET_KEY', 'dev-integration-script')

from app import app, db
import models
from services.lab_parser_service import LabZipParser, save_manifest_to_db

ZIPS = [
    "/mnt/user-data/uploads/techcorp-idor-HACK_THE_AI.zip",
    "/mnt/user-data/uploads/techcorp-info-disclosure-HACK_THE_AI-UPDATED.zip",
    "/mnt/user-data/uploads/Lab_4_The_Strange_Support_Ticket.zip",
    "/mnt/user-data/uploads/Lab_5_The_Suspicious_Email__1_.zip",
]

with app.app_context():
    db.create_all()
    admin_user = models.User.query.filter_by(username='admin').first()
    user_id = admin_user.id if admin_user else None

    upload_dir = app.config.get('LAB_UPLOAD_DIR', os.path.join(os.path.dirname(__file__), 'data', 'uploaded_labs'))
    os.makedirs(upload_dir, exist_ok=True)

    parser = LabZipParser(
        max_decompressed_size=app.config.get('LAB_MAX_ZIP_DECOMPRESSED_SIZE', 500*1024*1024),
        max_file_count=app.config.get('LAB_MAX_ZIP_FILE_COUNT', 10000),
    )

    results = []
    for zpath in ZIPS:
        name = os.path.basename(zpath)
        print(f"\n=== Processing {name} ===")

        validation = parser.validate_zip(zpath)
        print("Validation:", json.dumps(validation.to_dict(), indent=2)[:1500])
        if not validation.valid:
            print(f"SKIPPING {name}: validation failed")
            results.append((name, None, 'VALIDATION_FAILED'))
            continue

        extract_dir = os.path.join(upload_dir, f'lab_{uuid.uuid4().hex[:12]}')
        try:
            manifest = parser.parse_zip(zpath, extract_dir)
        except Exception as e:
            import traceback; traceback.print_exc()
            results.append((name, None, f'PARSE_ERROR: {e}'))
            continue

        print("Manifest title:", manifest.title, "| category:", manifest.category,
              "| missions:", len(manifest.missions), "| flags:", len(manifest.flags),
              "| target_app_path:", manifest.target_app_path)

        lab = save_manifest_to_db(manifest, extract_dir, user_id=user_id)
        db.session.commit()

        # Publish immediately
        lab.status = 'published'
        db.session.commit()

        print(f"Saved as lab id={lab.id}, status={lab.status}")
        results.append((name, lab.id, 'OK'))

    print("\n\n=== SUMMARY ===")
    for name, lab_id, status in results:
        print(f"{name}: {status} (lab_id={lab_id})")
