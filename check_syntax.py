try:
    import main
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
except SystemExit:
    print("SystemExit caught")
