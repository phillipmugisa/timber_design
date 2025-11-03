from design import design_a_member, perform_specific_check, display_results

if __name__ == '__main__':
    option = input("Design for a member(M) or perform specific check (S): ")
    results = design_a_member() if option == 'M' else perform_specific_check()
    display_results(results)

