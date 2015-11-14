import random
import click
import slimit.parser
import slimit.ast
import slimit.visitors.nodevisitor


@click.command()
@click.argument('infile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def main(infile, outfile):
    src = infile.read()

    with open('usernames.txt', 'r') as f:
        usernames = f.read().split('\n')
    random.shuffle(usernames)
    usernames = [u.replace('-', '_') for u in usernames]

    tree = slimit.parser.Parser().parse(src)
    nodes = [n for n in slimit.visitors.nodevisitor.visit(tree)]

    # Identify all variable declarations
    decl_idents = [n for n in nodes if isinstance(n, slimit.ast.VarDecl)]
    decl_idents = [n.children()[0].value for n in decl_idents]

    # Assign r/trees usernames to variable declarations
    ident_map = dict(zip(decl_idents, usernames))

    # Replace all usages of these idents with their corresponding usernames
    all_idents = [n for n in nodes if isinstance(n, slimit.ast.Identifier)]
    for ident in all_idents:
        ident.value = ident_map.get(ident.value) or ident.value

    src_transformed = tree.to_ecma()

    outfile.write(src_transformed)


if __name__ == '__main__':
    main()
