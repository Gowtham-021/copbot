from app import generate_crime_types_response, generate_fir_response
print('Crime types (ta):')
print(generate_crime_types_response('ta')[:1000])
print('\nFIR (ta):')
print(generate_fir_response('ta')[:500])
