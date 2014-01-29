CREATE SERVER cov_srv foreign data wrapper multicorn options (
    wrapper 'multicorn.covfdw.CovFdw'
);