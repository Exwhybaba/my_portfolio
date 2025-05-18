try:
    print("Launching DashTools GUI...")
    from dashtools.dashboard.dashboard import run_dashboard
    run_dashboard()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc() 