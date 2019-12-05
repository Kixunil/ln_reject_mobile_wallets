LN reject mobile wallets
========================

Rejects attempts to open a Lightning channel from mobile (or other non-forwarding) wallets.

How it works
------------

If the wallet has no public channels and the channel it attempts to open is not public, we assume it's not a forwarding node and so reject the channel opening.

Currently it supports only lnd `ChannelAcceptor`.

Why
---

If you know me as a huge fan of LN, you might find a project like this surprising. Let me explain. Lightning as any free market ecosystem consists of various businesses. Among other properties, the businesses differ in their liquidity - how much cash they hold at particular time.

Businesses with large liquidity are not too concerned with having some portion of their money locked up for some time, especially if the money is deflationary and they earn something on top of that. However, businesses that don't have much liquidity need to be more careful about locking up money, as they need to pay the suppliers.

There are also two kinds of LN wallets: forwarding and non-forwarding wallets. The key feature of a forwarding wallet is the ability of other participants of LN to route payments through it at (almost) any time. In contrast, one can't route payments through e.g. a mobile wallet.

When someone connects to a node of a less liquid business, it matters what kind of wallet it is. If the wallet is not forwarding, the business might run into a trouble if the connected peer makes substantial payment. Regardless of the business being the destination or not.

Thus a less liquid business might be interested in rejecting connection attempts from non-forwarding wallets. This is completely fine when it comes to functioning of LN, as the customer might connect to a forwarding node of a HODLer, who would forward his payment, earning fees for providing liquidity service.

[Paralelná Polis](https://paralelnapolis.sk) is one such "business" (actually a non-profit). As a young organization, it doesn't have large reserves, which sometimes poses a problem when attempting to pay the suppliers. This is amplified in times of Bitcoin price drop. On the other hand, it has many fans with public LN nodes who are hodling and don't mind to provide some liquidity.

If you want to open a channel with Paralelná Polis, you can open a public one or open with someone who has a public channel with Paralelná Polis (such as [the author](https://deb.ln-ask.me) of this script, who operates an LN node with reliable connection to Paralelná Polis). This has additional benefits to you as well. It improves your privacy and makes it less likely that the channel will have to be closed.

Note that we will NOT proactively close existing channels that violate the conditions in this script, but if it becomes necessary, those channels will be the top candidates for closing.

Usage
-----

Just run `python3 lnd_acceptor.py` under the same user you run `lnd` under.

If you consider the project useful, you can donate some sats by running `python3 lnd_acceptor.py --donate AMOUNT MEMO`

`AMOUNT` and `MEMO` are optional, `AMOUNT` is in sats and defaults to `50000`

License
-------

MITNFA
