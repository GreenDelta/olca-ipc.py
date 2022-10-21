import olca as ipc
import olca_schema as schema
import olca_schema.results as results


def main():
    client = ipc.Client(8080)
    setup = results.CalculationSetup(
        target=schema.Ref(
            id='7d1cbce0-b5b3-47ba-95b5-014ab3c7f569',
            model_type=schema.ModelType.PRODUCT_SYSTEM.value),
        amount=1)
    result = client.calculate(setup)
    state = result.wait_until_ready()
    if state.error:
        print(f'calculation failed: {state.error}')
        return

    result.dispose()
    print(result.get_state())


if __name__ == '__main__':
    main()
