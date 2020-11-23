for x in 1 2
    do
        # python3 lib/bulk_job_text.py
        python3 lib/common_lex.py
        python3 lib/mangonel.py

        if test -f "temp/.install"; then
            echo "Some or all modules are missing. Installing requirements.txt ..."
            pip3 install -r requirements.txt    
            rm "temp/.install"
        else
            echo "All required modules are present."
            break
        fi
    done