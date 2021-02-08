for x in 1 2
    do
        python3 lib/check_packages.py
        if test -f "temp/.install"; then
            echo "Some or all modules are missing. Running installs ..."
            pip3 install -r requirements.txt    
            rm "temp/.install"
        else
            break
        fi
    done

python3 lib/bulk_job_text.py
python3 lib/common_lex.py
python3 lib/match.py