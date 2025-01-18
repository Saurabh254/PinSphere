alembic downgrade base
echo "Downgraded to base, waiting 5 sec before upgrade"
sleep 5
alembic upgrade head
echo "Upgraded to head"
