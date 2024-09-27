from src.models.schedule import Event, Schedule

SCHEDULES: list[Schedule] = [
    Schedule(
        id=1,
        name='Everyday',
        description='One full session everyday',
        monday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        tuesday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        wednesday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        thursday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        friday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        saturday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        sunday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
    ),
    Schedule(
        id=2, 
        name='Weekdays Only',
        description='One full session everyday except weekends',
        monday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        tuesday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        wednesday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        thursday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        friday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
    ),
    Schedule(
        id=3, 
        name='1 day on, 1 day off',
        description='One full session every other day',
        monday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        wednesday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
        friday=[Event('Start', '09:00'), Event('Vote', '17:00'), Event('End', '23:00')],
    ),
    Schedule(
        id=4, 
        name='2-days sessions',
        description='One day to participate, one day to vote',
        monday=[Event('Start', '09:00'), Event('Vote', '21:00')],
        tuesday=[Event('End', '23:00')],
        wednesday=[Event('Start', '09:00'), Event('Vote', '21:00')],
        thursday=[Event('End', '23:00')],
        friday=[Event('Start', '09:00'), Event('Vote', '21:00')],
        saturday=[Event('End', '23:00')],
    ),
    Schedule(
        id=5, 
        name='Weekly Session',
        description='Theme on monday and votes on Thursday',
        monday=[Event('Start', '09:00')],
        thursday=[Event('Vote', '09:00')],
        sunday=[Event('End', '09:00')],
    )
]