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

    envi_val = result.get_total_flows()[0]
    print(envi_val)
    print(result.get_total_flow_value_of(envi_val.envi_flow))

    # do not forget to dispose a result
    # when you do not need it anymore
    result.dispose()


if __name__ == '__main__':
    main()
